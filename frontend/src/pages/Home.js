import React from 'react';
import { Link } from 'react-router-dom';
import { BsHouse, BsHeart, BsPerson } from 'react-icons/bs';
import { FaCrown } from 'react-icons/fa';
import '../styles/home.css';

function Home() {
    return (
        <div className="flex flex-col min-h-screen">
            <header className="text-black py-4 px-6 flex items-center justify-between">
                <div className="font-bold text-xl text-rose-400">Fairy</div>
            </header>
            <div className="flex-grow px-6 py-4">
                <p className="text-lg font-bold mb-2">???님,</p>
                <p className="text-lg font-bold">환영합니다!</p>
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
                <div className="mt-80">
                    <div className="flex">
                        <span className="mb-3 font-bold text-lg">순위</span>
                        <FaCrown className="ml-2 mt-1 text-xl text-yellow-500 mr-2"></FaCrown>
                    </div>
                    <div className="shadow p-2 flex justify-between mb-2">
                        <span>신은섭</span>
                        <span className="text-gray-400">90점</span>
                    </div>
                    <div className="shadow p-2 flex justify-between mb-2">
                        <span>송준일</span>
                        <span className="text-gray-400">89점</span>
                    </div>
                    <div className="shadow p-2 flex justify-between">
                        <span>성훈</span>
                        <span className="text-gray-400">87점</span>
                    </div>
                </div>
            </div>
            <div className="bg-white p-3 shadow-lg flex justify-around fixed bottom-0 left-0 right-0">
                <button className="p-3 rounded-full hover:bg-gray-100">
                    <BsHouse size={24} />
                </button>
                <button className="p-3 rounded-full hover:bg-gray-100">
                    <BsHeart size={24} />
                </button>
                <button className="p-3 rounded-full hover:bg-gray-100">
                    <BsPerson size={24} />
                </button>
            </div>
        </div>
    );
}

export default Home;