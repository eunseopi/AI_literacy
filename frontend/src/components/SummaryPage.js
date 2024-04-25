import React, { useState, useEffect } from 'react';
import {useNavigate} from "react-router-dom";

const SummaryPage = () => {
    const [randomText, setRandomText] = useState('');
    const [userSummary, setUserSummary] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const generateRandomText = () => {
            const randomText = '오늘은 지구의 생일이라고 불리는 지구의 날입니다.\n' +
                '\n' +
                '지구의 날은 환경 문제에 대한 관심을 높이기 위해 1970년에 처음 제정된 이후 전 세계 많은 국가에서 이를 기념하는 행사를 진행하고 있습니다.\n' +
                '\n' +
                '지구에게 생일 선물이 될 만한 우리의 노력에는 어떤 게 있을까요?\n' +
                '\n' +
                '오늘의 뉴스메이커에서 짚어보겠습니다.\n' +
                '\n' +
                '\n' +
                '지구의 날은, 1969년 미국 캘리포니아주에서 발생한 해상원유 유출 사고를 계기로 시작됐습니다.\n' +
                '\n' +
                '당시 해상에서 원유 시추 작업을 하던 중 시설이 파열되면서 무려 10만 배럴의 원유가 유출되자, 환경오염의 심각성이 대두됐고, 덩달아 환경 문제에 대한 전 세계적 관심도 생겨나기 시작했는데요.\n' +
                '\n' +
                '보시는 것처럼 당시 미국 전역에서 2천만 명의 어린이와 대학생, 시민들이 모였고 쓰레기를 줍는 행진과 각종 연설 등의 행사는 일주일간이나 계속되었죠.\n' +
                '\n' +
                '이후 지구의 날은 한국을 포함해 전 세계 192개국에서 약 7만 5,000여 개 기관과 단체에서 10억 명 이상의 시민들이 참여하는 글로벌 행사로 자리 잡았습니다.\n' +
                '\n' +
                '우리나라도 지구의 날을 맞아 2009년부터 환경오염을 막기 위한 노력의 일환으로, 기후변화 주간을 운영하고 있는데요.';
            setRandomText(randomText);
        };

        generateRandomText();
    }, []);

    const handleSubmit = () => {
        const score = calculateScore(userSummary, randomText);
        console.log('요약 점수:', score);

        alert(`요약 점수: ${score}`);

        navigate('/Home');
    };

    const calculateScore = (summary, text) => {
        return Math.floor(Math.random() * 101);
    }

    return (
        <div className="flex flex-col iㅞtems-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-8">오늘의 글</h1>
            <p className="text-lg mb-4">{randomText}</p>
            <textarea
                className="w-full max-w-md p-2 mb-4 ml-6 border border-gray-300 rounded"
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