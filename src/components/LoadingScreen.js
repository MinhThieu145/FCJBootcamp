import React from 'react';

function LoadingScreen(props) {
    // the function when the button is clicked
    const modalOpenHandler = () => {
        props.onModalOpen();
    }

    return (
        // first thing first. A background that half of the screen
        <div className="h-screen flex items-center justify-center">
            <div className="bg-white w-2/3 h-1/2 rounded-lg shadow-sm shadow-white flex items-center justify-center">
                {/* Cool loading animation */}
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-500 rounded-full animate-pulse"></div>
                    <div className="w-8 h-8 bg-green-500 rounded-full animate-pulse"></div>
                    <div className="w-8 h-8 bg-red-500 rounded-full animate-pulse"></div>
                </div>
            </div>
        </div>
    );
}

export default LoadingScreen;
