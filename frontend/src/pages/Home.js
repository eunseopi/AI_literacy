import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
import { FaCrown } from 'react-icons/fa';
import '../styles/home.css';
import Footer from "../components/Footer";

function Home() {
    const [continuousDays, setContinuousDays] = useState(null);
    const [nickName, setNickName] = useState("");
    const [score, setScore] = useState(0);
    const [rankings, setRankings] = useState([
        { name : '송준일', score: 8 },
        { name : '성훈', score: 6}
    ]);

    useEffect( () => {
        const fetchProfile = async () => {
            try{
                const token = localStorage.getItem("token");
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/profile`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setNickName(data.nick_name);
                } else {
                    throw new Error('닉네임 가져오기 실패');
                }
            } catch (error) {
                console.log('닉네임 가져오기 실패하였습니다.', error);
            }
        }

        const fetchContinuous = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/continuous_days`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setContinuousDays(data.continuous_days);
                } else {
                    throw new Error('연속 일자 가져오기 실패');
                }
            } catch (error) {
                console.log("연속 로그인 일자 가져오기 실패!");
            }
        };

        const fetchScore = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/avg_scores`, {
                    method: 'GET',
                    headers : {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setScore(data.average);
                } else {
                    throw new Error('점수 가져오기 실패');
                }
            } catch (error) {
                console.log("점수 가져오는거 실패~");
            }
        }

        fetchProfile();
        fetchContinuous();
        fetchScore();
    }, []);


    useEffect(() => {
        if (nickName && score) {
            const userRanking = { name: nickName, score: score };
            const updatedRankings = [...rankings, userRanking];
            updatedRankings.sort((a, b) => b.score - a.score);
            setRankings(updatedRankings);
        }
    }, [nickName, score]);

    return (
        <div className="flex flex-col min-h-screen">
            <header className="text-black py-4 px-6 flex items-center justify-between">
                <div className="font-bold text-xl text-rose-400">Fairy</div>
            </header>
            <div className="flex-grow px-6 py-4">
                <p className="text-lg font-bold mb-2">{nickName}님,</p>
                <p className="text-lg font-bold mb-2">환영합니다!</p>
                {continuousDays !== null &&
                    <p className="text-lg font-bold">{continuousDays}일째 접속 중입니다.</p>}
                <div className="shadow-xl p-6 flex justify-between items-center">
                    <div>
                        <span className="flex font-bold mt-3 text-xl">오늘의 글</span>
                        <div className="flex mt-14">
                            <p className="inline-block px-4 bg-pink-200 rounded-full font-light text-pink-600">주제: 문화</p>
                            <p className="ml-4 inline-block px-4 bg-pink-200 rounded-full font-light text-pink-600">난이도: 중</p>
                        </div>
                    </div>
                    <Link
                        to="/summary"
                        className="mt-20 inline-block px-6 py-3 bg-violet-400 text-white rounded-3xl hover:bg-violet-500"
                    >
                        도전하러가기 ->
                    </Link>
                </div>
                <div className="mt-72">
                    <div className="flex">
                        <span className="mb-3 font-bold text-lg">순위</span>
                        <FaCrown className="ml-2 mt-1 text-xl text-yellow-500 mr-2"></FaCrown>
                    </div>
                    {rankings.map((ranking, index) => (
                        <div key={index} className="shadow p-2 flex justify-between mb-2">
                            <span>{ranking.name}</span>
                            <span className="text-gray-400">{ranking.score}점</span>
                        </div>
                    ))}
                </div>
            </div>
            <Footer/>
        </div>
    );
}

export default Home;