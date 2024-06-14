import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Summaries() {
    const [savedSummaries, setSavedSummaries] = useState([]);
    const [selectedSummary, setSelectedSummary] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const token = localStorage.getItem('token');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchSummaries = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/history`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setSavedSummaries(data);
                } else {
                    throw new Error('요약글 불러오기 실패');
                }
            } catch (error) {
                console.error('요약글 불러오기 중 에러 발생:', error);
            }
        };

        fetchSummaries();
    }, [token]);

    const handleSummaryClick = (summary) => {
        setSelectedSummary(summary);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setSelectedSummary(null);
    };

    return (
        <div className="flex flex-col min-h-screen">
            <header className="bg-white py-4 px-6 flex items-center justify-between shadow-md">
                <div className="font-bold text-2xl text-rose-400">나의 요약글</div>
                <button className="hover:bg-gray-100 rounded-full p-2" onClick={() => navigate(-1)}>
                    뒤로가기
                </button>
            </header>
            <main className="flex-grow bg-gray-100 p-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-lg font-bold mb-4">저장된 요약글 목록</h2>
                    <div className="flex flex-col space-y-4">
                        {savedSummaries.map((summary, index) => (
                            <div
                                key={index}
                                className="bg-gray-100 rounded-lg p-4 flex items-center justify-between cursor-pointer"
                                onClick={() => handleSummaryClick(summary)}
                            >
                                <span className="text-sm text-gray-500">{summary.user_summary}</span>
                                <span className="font-bold text-rose-400">{summary.score} 점</span>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
            {showModal && selectedSummary && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                    <div className="bg-white p-8 rounded shadow-lg">
                        <h2 className="text-lg font-bold mb-4">요약 상세</h2>
                        <p className="mb-2"><strong>날짜:</strong> {selectedSummary.played_date}</p>
                        <p className="mb-2"><strong>점수:</strong> {selectedSummary.score}</p>
                        <p className="mb-2"><strong>요약:</strong> {selectedSummary.user_summary}</p>
                        <p className="mb-2"><strong>댓글:</strong> {selectedSummary.comment}</p>
                        <p className="mb-2"><strong>LLM 요약:</strong> {selectedSummary.llm_summary}</p>
                        <p className="mb-2"><strong>문서 URL:</strong> <a href={selectedSummary.docurl} target="_blank" rel="noopener noreferrer">{selectedSummary.docurl}</a></p>
                        <button
                            className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded mt-4"
                            onClick={closeModal}
                        >
                            닫기
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Summaries;
