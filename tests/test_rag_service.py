import unittest
from unittest.mock import patch, MagicMock
from collections import namedtuple
Document = namedtuple("Document", ["page_content"])

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.rag_service import RAGService


class TestRAGService(unittest.TestCase):

    @patch('services.rag_service.ModelManager')
    def setUp(self, MockModelManager):
        self.mock_model_manager = MockModelManager.return_value
        self.mock_model_manager.initialize_models.return_value = True
        self.rag_service = RAGService()

    @patch('services.rag_service.PyPDFLoader')
    @patch('services.rag_service.Chroma')
    @patch('services.rag_service.RecursiveCharacterTextSplitter')
    def test_process_document_success(self, MockSplitter, MockChroma, MockLoader):
        # Create a mock document object
        mock_document = Document(page_content="This is a mock document content.")
        mock_loader_instance = MockLoader.return_value
        mock_loader_instance.load.return_value = [mock_document]
        
        # Setup the mock splitter
        mock_splitter_instance = MockSplitter.return_value
        mock_splitter_instance.split_documents.return_value = [mock_document]  # Return the same document
        
        mock_chroma_instance = MockChroma.return_value
        mock_chroma_instance.as_retriever.return_value = "mock retriever"
        
        # Set up the Chroma.from_documents method
        MockChroma.from_documents.return_value = mock_chroma_instance
        
        retriever = self.rag_service.process_document("dummy.pdf")
        
        # Assert that the methods were called correctly
        MockLoader.assert_called_once_with("dummy.pdf")
        mock_loader_instance.load.assert_called_once()
        mock_splitter_instance.split_documents.assert_called_once_with([mock_document])
        MockChroma.from_documents.assert_called_once()
        mock_chroma_instance.as_retriever.assert_called_once()
        
        # Assert that the retriever was returned
        self.assertEqual(retriever, "mock retriever")

    @patch('services.rag_service.PyPDFLoader')
    def test_process_document_failure(self, MockLoader):
        MockLoader.side_effect = Exception("Mock error")
        with self.assertRaises(Exception):
            self.rag_service.process_document("dummy.pdf")

    @patch('services.rag_service.RetrievalQA')
    @patch('services.rag_service.RAGService.process_document')
    def test_answer_query_success(self, MockProcessDocument, MockRetrievalQA):
        MockProcessDocument.return_value = 'mock retriever'
        mock_qa_instance = MockRetrievalQA.from_chain_type.return_value
        mock_qa_instance.invoke.return_value = {'result': 'Helpful Answer: This is a test answer.'}

        response = self.rag_service.answer_query("dummy.pdf", "test question")
        self.assertEqual(response, "This is a test answer.")

    @patch('services.rag_service.RAGService.process_document')
    def test_answer_query_failure(self, MockProcessDocument):
        MockProcessDocument.side_effect = Exception("Mock error")
        response = self.rag_service.answer_query("dummy.pdf", "test question")
        self.assertTrue(response.startswith("Error:"))

if __name__ == '__main__':
    unittest.main()
