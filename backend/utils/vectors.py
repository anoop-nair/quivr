from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from llm.qa import BrainPicking, BrainSettings
from llm.summarization import llm_evaluate_summaries, llm_summerize
from logger import get_logger
from models.chats import ChatMessage
from models.settings import BrainSettings
from pydantic import BaseModel
from utils.common import CommonsDep

logger = get_logger(__name__)

class Neurons(BaseModel):

    commons: CommonsDep
    settings = BrainSettings()
    
    def create_vector(self, user_id, doc, user_openai_api_key=None):
        logger.info(f"Creating vector for document")
        logger.info(f"Document: {doc}")
        if user_openai_api_key:
            self.commons['documents_vector_store']._embedding = OpenAIEmbeddings(openai_api_key=user_openai_api_key)
        try:
            sids = self.commons['documents_vector_store'].add_documents([doc])
            if sids and len(sids) > 0:
                self.commons['supabase'].table("vectors").update({"user_id": user_id}).match({"id": sids[0]}).execute()
        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_embedding(self, content):
        return self.commons['embeddings'].embed_query(content)

    def similarity_search(self, query, table='match_summaries', top_k=5, threshold=0.5):
        query_embedding = self.create_embedding(query)
        summaries = self.commons['supabase'].rpc(
            table, {'query_embedding': query_embedding,
                    'match_count': top_k, 'match_threshold': threshold}
        ).execute()
        return summaries.data


def create_summary(commons: CommonsDep, document_id, content, metadata):
    logger.info(f"Summarizing document {content[:100]}")
    summary = llm_summerize(content)
    logger.info(f"Summary: {summary}")
    metadata['document_id'] = document_id
    summary_doc_with_metadata = Document(
        page_content=summary, metadata=metadata)
    sids = commons['summaries_vector_store'].add_documents(
        [summary_doc_with_metadata])
    if sids and len(sids) > 0:
        commons['supabase'].table("summaries").update(
            {"document_id": document_id}).match({"id": sids[0]}).execute()


def get_answer(commons: CommonsDep, chat_message: ChatMessage, email: str, user_openai_api_key: str):
    Brain = BrainPicking().init(chat_message.model, email)
    qa = Brain.get_qa(chat_message, user_openai_api_key)

    neurons =  Neurons(commons=commons)

    if chat_message.use_summarization:
        summaries = neurons.similarity_search(chat_message.question, table='match_summaries')
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        if evaluations:
            response = commons['supabase'].from_('vectors').select(
                '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
            additional_context = '---\nAdditional Context={}'.format(
                '---\n'.join(data['content'] for data in response.data)
            ) + '\n'
            model_response = qa(
                {"question": additional_context + chat_message.question})
    else:
        transformed_history = []

        for i in range(0, len(chat_message.history) - 1, 2):
            user_message = chat_message.history[i][1]
            assistant_message = chat_message.history[i + 1][1]
            transformed_history.append((user_message, assistant_message))
        model_response = qa({"question": chat_message.question, "chat_history": transformed_history})

    answer = model_response['answer']

    if "source_documents" in answer:
        sources = [
            doc.metadata["file_name"] for doc in answer["source_documents"]
            if "file_name" in doc.metadata]
        if sources:
            files = dict.fromkeys(sources)
            answer = answer + "\n\nRef: " + "; ".join(files)

    return answer