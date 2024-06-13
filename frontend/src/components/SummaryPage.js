import React, { useState, useEffect } from 'react';
import {Link, useNavigate} from "react-router-dom";

const SummaryPage = () => {
    const [content, setContent] = useState('');
    const [userSummary, setUserSummary] = useState('');
    const [llmSummary, setLlmSummary] = useState('');
    const [score, setScore] = useState(null);
    const [comment, setComment] = useState('');
    const [docUrl, setDocUrl] = useState('');
    const [day, setDay] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const [remaningTime, setRemaningTime] = useState(300);
    const navigate = useNavigate();

    useEffect(() => {
        const generateText = async () => {
            try {
                const response = await fetch('http://dev.cemi.re.kr:8888/get_contents', {
                    method: 'GET',
                });

                if (response.ok) {
                    const data = await response.json();
                    setContent(data.content);
                } else {
                    throw new Error('서버 응답에 문제가 있습니다.');
                }
            } catch (error) {
                console.error('랜덤 텍스트 요청 중 에러 발생:', error);
                alert('랜덤 텍스트 요청 중 에러가 발생했습니다.');
            }
        };

        generateText();

    const timer = setInterval(() => {
        setRemaningTime((prevTime) => prevTime -1 );
    }, 1000);

    setTimeout(()=> {
        navigate('/Home');
    }, 300000);

    return () => {
        clearInterval(timer);
        };
    }, [navigate]);

    const handleSubmit = async () => {
        setLoading(true);

        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://dev.cemi.re.kr:8888/literacy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ user_input: userSummary }),
            });

            if (response.ok) {
                const data = await response.json();
                setDay(data.played_date);
                setLlmSummary(data.llm_summary);
                setUserSummary(data.user_summary);
                setScore(data.score);
                setComment(data.comment);
                setDocUrl(data.docurl);
                setShowModal(true);
            } else {
                throw new Error('서버 응답에 문제가 있습니다.');
            }
        } catch (error) {
            console.error('서버 요청 중 에러 발생:', error);
            alert('서버 요청 중 에러가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    const closeModal = () => {
        setShowModal(false);
        navigate('/Home');
    };

    const formatTime = (timeInSeconds) => {
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = timeInSeconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="absolute top-4 left-4">
                <Link to="/Home" className="text-pink-600 hover:text-pink-800 transition-colors duration-300">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                              d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                    </svg>
                </Link>
            </div>
            <h1 className="text-4xl font-bold mb-8 text-pink-600">오늘의 글</h1>
            <div className="mb-4 ml-80 text-lg font-bold text-pink-500">
                남은 시간: <span>{formatTime(remaningTime)}</span>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-md max-h-96 overflow-y-auto mb-5">
                <p className="text-lg leading-relaxed">{content}</p>
            </div>
            <textarea
                className="w-full max-w-md p-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                placeholder="요약을 입력하세요"
                value={userSummary}
                onChange={(e) => setUserSummary(e.target.value)}
                rows={4}
            />
            <button
                className="bg-pink-600 hover:bg-pink-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-300"
                onClick={handleSubmit}
                disabled={loading}
            >
                {loading ? '제출 중...' : '제출하기'}
            </button>
            {showModal && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                    <div className="bg-white p-8 rounded shadow-lg max-w-md w-full">
                        <div className="mb-5">
                            <h2 className="text-xl font-bold mb-2">요약 결과</h2>
                            <div className="border-t border-gray-200 pt-2">
                                <p className="text-sm font-semibold">날짜: <span
                                    className="font-normal">{day}</span></p>
                            </div>
                            <div className="border-t border-gray-200 pt-2">
                                <p className="text-sm font-semibold">요약 점수: <span
                                    className="font-normal">{score}점</span></p>
                            </div>
                            <div className="border-t border-gray-200 pt-2">
                                <h3 className="text-sm font-semibold">LLM 요약:</h3>
                                <p className="text-sm font-normal">{llmSummary}</p>
                            </div>
                            <div className="border-t border-gray-200 pt-2">
                                <h3 className="text-sm font-semibold">사용자 요약:</h3>
                                <p className="text-sm font-normal">{userSummary}</p>
                            </div>
                            <div className="border-t border-gray-200 pt-2">
                                <h3 className="text-sm font-semibold">총평:</h3>
                                <p className="text-sm font-normal">{comment}</p>
                            </div>
                        </div>
                        <div className="border-t border-gray-200 pt-4">
                            <h3 className="text-sm font-semibold">문서 URL:</h3>
                            <p className="text-sm font-normal">
                                <a href={docUrl} className="text-blue-500 underline">{docUrl}</a>
                            </p>
                        </div>
                        <div className="text-center">
                            <button
                                className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-3 px-10 rounded-lg mt-4"
                                onClick={closeModal}
                            >
                                확인
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SummaryPage;
