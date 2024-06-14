import React, {useState} from 'react';
import {useNavigate} from "react-router-dom";

const SignUpPage = () => {
    const [email, setEmail] = useState('');
    const [nickName, setNickName] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate = useNavigate();


    const handleSignUp = async () => {
        try {
            if (password !== confirmPassword) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }

            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email , password, nick_name: nickName }),
            });

            if (response.status === 200) {
                navigate('/');
            }
        } catch (error) {
            console.error('회원가입 중 에러 발생:', error);
            alert('회원가입 중 에러가 발생했습니다.');
        }
    };



    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4">
            <div className="flex items-center mb-10">
                <h1 className="text-4xl font-bold text-pink-500 font-caveat">Fairy</h1>
            </div>
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-500">회원가입</h2>
            </div>
            <div className="w-96 max-w-md">
                <div className="flex items-center mb-4 border rounded-md px-3 py-4">
                    <input
                        type="text"
                        placeholder="이메일"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value)
                        }}
                        className="w-full outline-none"
                    />
                </div>
                <div
                    className={`flex items-center mb-4 border rounded-md px-3 py-4`}>
                    <input
                        type="text"
                        placeholder="닉네임"
                        value={nickName}
                        onChange={(e) => {
                            setNickName(e.target.value)
                        }}
                        className="w-full outline-none"
                    />
                </div>
                <div className="flex items-center mb-4 border rounded-md px-3 py-4">
                    <input
                        type="password"
                        placeholder="비밀번호"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value)
                        }}
                        className="w-full outline-none"
                    />
                </div>
                <div
                    className={`flex items-center mb-4 border rounded-md px-3 py-4 ${password !== confirmPassword && confirmPassword !== '' ? 'border-red-500' : ''}`}>
                    <input
                        type="password"
                        placeholder="비밀번호 확인"
                        value={confirmPassword}
                        onChange={(e) => {
                            setConfirmPassword(e.target.value)
                        }}
                        className="w-full outline-none"
                    />
                </div>
            </div>
            <button
                onClick={handleSignUp}
                className="bg-blue-500 hover:bg-blue-700 text-white text-center font-bold py-3 px-4 w-96 rounded focus:outline-none focus:shadow-outline"
            >
                회원가입
            </button>
        </div>

    )
}
export default SignUpPage;