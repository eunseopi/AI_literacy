import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

const SummaryPage = () => {
    const [randomText, setRandomText] = useState('');
    const [userSummary, setUserSummary] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const generateRandomText = async () => {
            try {
                const response = await fetch('http://dev.cemi.re.kr:8888/literacy', {
                    method: 'GET',
                });

                if (response.ok) {
                    const data = await response.json();
                    const { randomText } = data;
                    setRandomText(randomText);
                } else {
                    throw new Error('서버 응답에 문제가 있습니다.');
                }
            } catch (error) {
                console.error('랜덤 텍스트 요청 중 에러 발생:', error);
                alert('랜덤 텍스트 요청 중 에러가 발생했습니다.');
            }
        };

        generateRandomText();
    }, []);

    const handleSubmit = async () => {
        try {
            const response = await fetch('http://dev.cemi.re.kr:8888/literacy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userSummary }),
            });

            if (response.ok) {
                const data = await response.json();
                // 서버에서 받은 데이터를 처리
                const { score } = data;
                alert(`요약 점수: ${score}`);
                navigate('/Home');
            } else {
                throw new Error('서버 응답에 문제가 있습니다.');
            }
        } catch (error) {
            console.error('서버 요청 중 에러 발생:', error);
            alert('서버 요청 중 에러가 발생했습니다.');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-8">오늘의 글</h1>
            <p className="text-lg mb-4">{randomText}</p>
            <textarea
                className="w-full max-w-md p-2 mb-4 border border-gray-300 rounded"
                placeholder="요약을 입력하세요"
                value={userSummary}
                onChange={(e) => setUserSummary(e.target.value)}
                rows={4}
            />
            <button
                className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded"
                onClick={handleSubmit}
            >
                제출하기
            </button>
        </div>
    );
};

export default SummaryPage;
