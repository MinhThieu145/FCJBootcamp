import React from 'react';

const ArticleDisplay = ({ article }) => {
    return (
        <div className="h-full flex justify-center items-center">
            <div className='bg-white rounded-lg shadow-md p-6 max-w-4xl'>
                <h1 className="text-2xl font-bold mb-4">{article.title}</h1>
                <div className="overflow-auto max-h-96">
                    <p className="text-gray-700 leading-relaxed">{article.content}</p>
                </div>
            </div>
        </div>
    );
};

export default ArticleDisplay;
