import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import { DocumentItem } from '../types';
import { Upload, FileText, Trash2, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const fetchDocs = async () => {
    try {
      const res = await apiClient.get('/api/v1/documents');
      setDocuments(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    setStatusMsg(null);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await apiClient.post('/api/v1/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatusMsg("Document uploaded, encrypted (AES-256), and indexed into ChromaDB successfully!");
      setSelectedFile(null);
      fetchDocs();
    } catch (err: any) {
      setStatusMsg(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiClient.delete(`/api/v1/documents/${id}`);
      fetchDocs();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Document Intelligence & Vault</h2>
        <p className="text-slate-500 text-sm">Upload financial contracts, loan disclosures, and bank statements for clause extraction and RAG indexing.</p>
      </div>

      {/* Upload Box */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <form onSubmit={handleUpload} className="flex flex-col md:flex-row items-center gap-4">
          <input
            type="file"
            accept=".pdf,.txt,.docx"
            onChange={(e) => setSelectedFile(e.target.files ? e.target.files[0] : null)}
            className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100"
          />
          <button
            type="submit"
            disabled={!selectedFile || uploading}
            className="w-full md:w-auto px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium text-sm transition-colors flex items-center justify-center disabled:opacity-50"
          >
            <Upload className="w-4 h-4 mr-2" />
            {uploading ? "Encrypting & Indexing..." : "Upload Document"}
          </button>
        </form>
        {statusMsg && (
          <p className="mt-3 text-sm text-emerald-600 flex items-center">
            <CheckCircle2 className="w-4 h-4 mr-1.5" /> {statusMsg}
          </p>
        )}
      </div>

      {/* Document List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <h3 className="font-semibold text-slate-800 text-sm">Indexed Document Repository</h3>
          <span className="text-xs text-slate-500">{documents.length} Files</span>
        </div>
        <div className="divide-y divide-slate-200">
          {documents.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-sm">
              No documents uploaded yet. Upload a PDF, TXT, or DOCX above to begin.
            </div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="p-4 flex items-center justify-between hover:bg-slate-50">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-900">{doc.filename}</p>
                    <div className="flex items-center space-x-3 text-xs text-slate-500 mt-0.5">
                      <span>{(doc.file_size / 1024).toFixed(1)} KB</span>
                      <span>{doc.page_count} Pages</span>
                      <span>{doc.chunk_count} Chunks</span>
                      <span className="text-emerald-600 font-medium flex items-center">
                        <ShieldCheck className="w-3 h-3 mr-1" /> AES-256 Vault
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-slate-400 hover:text-red-600 p-2 rounded-lg"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
