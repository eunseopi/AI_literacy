import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import { BsGear, BsCamera } from "react-icons/bs";
import { useNavigate } from "react-router-dom";

function Profile() {
    const [profileImage, setProfileImage] = useState(null);
    const [email, setEmail] = useState("");
    const [nickName, setNickName] = useState("");
    const [imageUrl, setImageUrl] = useState("");
    const [savedSummaries, setSavedSummaries] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/profile`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    if (data.profile_image_url) {
                        setProfileImage(data.profile_image_url);
                        setNickName(data.nick_name);
                    }
                    setEmail(data.email);
                } else {
                    throw new Error('프로필 불러오기 실패');
                }
            } catch (error) {
                console.error('프로필 불러오기 실패 이유:', error);
            }
        };

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

        fetchProfile();
        fetchSummaries();
    }, [token]);

    const handleImageUpload = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/update_profile_img`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ update_img: imageUrl }),
            });

            if (response.ok) {
                const data = await response.json();
                setProfileImage(data.updated_img);
            } else {
                throw new Error('사진 업로드 실패');
            }
        } catch (error) {
            console.log('이미지 업로드 에러:', error);
            alert('이미지 업로드 에러.');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    }

    const toggleModal = () => {
        setShowModal(!showModal);
    }
    return (
        <div className="flex flex-col min-h-screen">
            <header className="bg-white py-4 px-6 flex items-center justify-between shadow-md">
                <div className="font-bold text-2xl text-rose-400">마이페이지</div>
                <button className="hover:bg-gray-100 rounded-full p-2" onClick={toggleModal}>
                    <BsGear size={24}/>
                </button>
            </header>
            <main className="flex-grow bg-gray-100 p-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center mb-4">
                        <div className="relative">
                            <div
                                className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center text-xl text-gray-500">
                                {profileImage ? (
                                    <img
                                        src={`${profileImage}`}
                                        alt="Profile"
                                        className="w-20 h-20 rounded-full object-cover"
                                    />
                                ) : (
                                    <span>( ˶ˆᗜˆ˵ )</span>
                                )}
                            </div>
                            <label
                                htmlFor="image-url-input"
                                className="absolute bottom-0 right-0 bg-gray-200 rounded-full p-1 cursor-pointer"
                            >
                                <BsCamera
                                    onClick={handleImageUpload}
                                    size={16}/>
                            </label>
                            <input
                                id="image-url-input"
                                type="text"
                                placeholder="사진 URL 입력"
                                value={imageUrl}
                                onChange={(e) => setImageUrl(e.target.value)}
                            />
                        </div>
                        <div className="ml-4">
                            <h2 className="text-lg font-bold">{nickName}</h2>
                            <p className="text-gray-500">{email}</p>
                            <div className="flex items-center mt-2"></div>
                        </div>
                    </div>
                    <div className="flex flex-col space-y-4">
                        <div
                            className="bg-gray-100 rounded-lg p-4 flex items-center justify-between cursor-pointer"
                            onClick={() => navigate('/summaries')}
                        >
                            <span>나의 요약글</span>
                            <span className="text-rose-400 font-bold">{savedSummaries.length} 개</span>
                        </div>
                        <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-between">
                            <span className="text-gray-500">댓글</span>
                            <span className="font-bold text-rose-400 text-center">0 개</span>
                        </div>
                        <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-between">
                            <span className="text-gray-500">좋아요</span>
                            <span className="font-bold text-rose-400 text-center">0 개</span>
                        </div>
                    </div>
                </div>
            </main>
            <Footer/>
            {showModal && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                    <div className="grid bg-white p-3 rounded shadow-lg max-w-md w-72">
                        <button
                            className="mb-3 place-self-end"
                            onClick={toggleModal}
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>

                        <button
                            className="bg-rose-300 hover:bg-rose-500 text-white font-bold py-3 px-6 ml-2 mr-2 mb-3 rounded-lg transition-colors duration-300"
                            onClick={handleLogout}
                        >
                            로그아웃
                        </button>
                        <button
                            className="bg-rose-300 hover:bg-rose-500 text-white font-bold py-3 px-6 ml-2 mr-2 rounded-lg transition-colors duration-300"
                        >
                            프로필 수정
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Profile;
