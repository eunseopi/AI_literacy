import React, { useState } from "react";
import Footer from "../components/Footer";
import { BsGear, BsCamera } from "react-icons/bs";

function Profile() {
    const [profileImage, setProfileImage] = useState(null);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        setProfileImage(URL.createObjectURL(file));
    };

    return (
        <div className="flex flex-col min-h-screen">
            <header className="bg-white py-4 px-6 flex items-center justify-between shadow-md">
                <div className="font-bold text-2xl text-rose-400">마이페이지</div>
                <button className="hover:bg-gray-100 rounded-full p-2">
                    <BsGear size={24} />
                </button>
            </header>
            <main className="flex-grow bg-gray-100 p-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center mb-4">
                        <div className="relative">
                            <div className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center text-xl text-gray-500">
                                {profileImage ? (
                                    <img
                                        src={profileImage}
                                        alt="Profile"
                                        className="w-20 h-20 rounded-full object-cover"
                                    />
                                ) : (
                                    <span>( ˶ˆᗜˆ˵ )</span>
                                )}
                            </div>
                            <label
                                htmlFor="image-upload"
                                className="absolute bottom-0 right-0 bg-gray-200 rounded-full p-1 cursor-pointer"
                            >
                                <BsCamera size={16} />
                            </label>
                            <input
                                id="image-upload"
                                type="file"
                                accept="image/*"
                                className="hidden"
                                onChange={handleImageUpload}
                            />
                        </div>
                        <div className="ml-4">
                            <h2 className="text-lg font-bold">닉네임</h2>
                            <p className="text-gray-500">s@abc.com(이메일)</p>
                            <div className="flex items-center mt-2"></div>
                        </div>
                    </div>
                    <div className="flex flex-col space-y-4">
                        <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-between">
                            <span>나의 요약글</span>
                            <span className="text-rose-400 font-bold">0 개</span>
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
            <Footer />
        </div>
    );
}

export default Profile;