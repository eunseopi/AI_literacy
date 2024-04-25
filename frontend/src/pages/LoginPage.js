import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();

        const validEmail = 'test@test.com';
        const validPassword = '1234';

        if (email === validEmail && password === validPassword) {
            navigate('/Home');
        } else {
            alert('이메일 또는 비밀번호가 틀렸습니다.');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-8 text-rose-400 font-caveat">Fariy</h1>
            <form onSubmit={handleLogin} className="w-full max-w-sm">
                <div className="mb-4">
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="이메일을 입력하세요."
                        className="shadow appearance-none border rounded w-full py-3 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>
                <div className="mb-6">
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="비밀번호"
                        className="shadow appearance-none border rounded w-full py-3 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 w-full rounded focus:outline-none focus:shadow-outline"
                >
                    로그인
                </button>
            </form>
            <div className="mt-4 flex">
                <p className="mr-2">계정이 없으신가요?</p>
                <Link
                    to="/SignUp"
                    className="font-bold text-blue-500">
                    가입하기
                </Link>
            </div>
        </div>
    );
}

export default LoginPage;