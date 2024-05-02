import React from 'react';
import { Link } from 'react-router-dom';
import { BsHouse, BsHeart, BsPerson } from 'react-icons/bs';

const Footer = () => {
    return (
        <div className="bg-white p-3 shadow-lg flex justify-around fixed bottom-0 left-0 right-0">
            <div>
                <Link to="/Home"
                      className="p-3 bg-white mt-1 bottom-0 left-0 right-0 flex justify-around rounded-full hover:bg-gray-100">
                    <BsHouse size={24}/>
                </Link>
            </div>
            <button className="p-3 mt-1.5 rounded-full hover:bg-gray-100 relative">
                <BsHeart size={24} />
            </button>
            <div>
                <Link to="/profile" className="p-3 bg-white mt-1 bottom-0 left-0 right-0 flex justify-around rounded-full hover:bg-gray-100">
                    <BsPerson size={24} />
                </Link>
            </div>
        </div>
    );
};

export default Footer;
