
function UploadFile(props) {

    // the function when the button is clicked
    const modalOpenHandler = () => {
        props.onModalOpen();
    }

    return (
        // first thing first. A background that half of the screen
        <div className="h-screen flex items-center justify-center">
            <div className="bg-white w-2/3 h-1/2 rounded-lg shadow-sm shadow-white">
                {/* Now the button and the icon*/}
                <div className="flex flex-col items-center justify-center h-full">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={0.75} stroke="currentColor" className="max-h-28 max-w-28">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" />
                    </svg>

                    {/* Okay. Now the button*/}
                    <button onClick={modalOpenHandler} className="w-36 bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded">
                        Translate Now
                    </button>
                </div>

            </div>

        </div>
    );
}

export default UploadFile;