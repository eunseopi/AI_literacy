import React, {useState} from 'react';
import {Link} from "react-router-dom";

const SignUpPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    // const navigate = useNavigate();


    // -------------- 백엔드 연결 시 쓸 코드입니다 ~~ ----------------
    // const handleSignUp = async () => {
    //     try {
    //         const response = await fetch('/api/signup', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({email, password}),
    //         });
    //
    //         if (response.ok) {
    //             // 회원가입 성공 했을 때 로그인 화면으로 넘어가기
    //             navigate('/Login');
    //         } else{
    //             // 이건 실패시
    //             alert('회원가입에 실패했습니다.');
    //         }
    //     } catch (error) {
    //         console.error('회원가입 중 에러 발생:', error);
    //     }
    // }


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
            <Link
                to="/"
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white text-center font-bold py-3 px-4 w-96 rounded focus:outline-none focus:shadow-outline"
            >
                회원가입
            </Link>

            {/* --------- 나중에 연결 하면 위에 코드 이 아래로 바꾸면 됩니다. ---------------*/}
            {/*<button*/}
            {/*    onClick={handleSignUp}*/}
            {/*    className="bg-blue-500 hover:bg-blue-700 text-white text-center font-bold py-3 px-4 w-96 rounded focus:outline-none focus:shadow-outline"*/}
            {/*>*/}
            {/*    회원가입*/}
            {/*</button>*/}
        </div>

    )
}
export default SignUpPage;