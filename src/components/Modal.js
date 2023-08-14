import React from 'react';
import ReactDOM from 'react-dom';
import { useState } from 'react';

// import the setup function from the FetchData.js file
import SendMessage from './FetchData';

const Backdrop = (props) => {
    return <div onClick={() => { console.log('please response') }} className="fixed insert-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full cursor-pointer z-0"></div>;
};

const ModalOverlay = (props) => {

    const [inputLink, setInputLink] = useState('')

    // state if the link is valid
    const [isValidLink, setIsValidLink] = useState(true);

    function handleData(data) {
        console.log('Received data:', data);
        // Do something with the received data
    }

    const okButtonHandler = (something) => {
        console.log(inputLink);

        // check if the link is valid
        // if not, show an error message
        // if yes, send the link to the backend
        // and then close the modal

        const urlPattern = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/i;
        const isValidUrl = urlPattern.test(inputLink);

        if (!isValidUrl) {
            setIsValidLink(false);
            return;
        }


        // close the modal
        something.onModalClose();
        // make the upload file component disappear
        something.onUploadFileClose();

        // open connection
        const ws = new WebSocket('wss://5fodc7y5ti.execute-api.us-east-1.amazonaws.com/production');

        // on message
        ws.onopen = () => {
            console.log('connected');

            // send the message
            ws.send(JSON.stringify({
                action: 'sendArticleUrl',
                articleUrl: inputLink
            }));

            // when receive a message
            ws.onmessage = async (event) => {

                // log the result
                console.log(event.data);

                // parse the result
                const result = await JSON.parse(event.data);
                console.log(result);

                console.log('Raw Article', result.rawObjectUrl);
                console.log('Translated Article', result.translatedPublicUrl);

                // fetch the translated article
                const translatedArticle = await fetch(result.translatedPublicUrl);

                // parse to json
                const translatedArticleJson = await translatedArticle.json();
                console.log(translatedArticleJson);

                // set the article
                something.onSetArticle(translatedArticleJson);

                // close the connection when done
                ws.close();

            }

            ws.onclose = () => {
                console.log('disconnected');
            }
        }


    }



    return (
        <div className="fixed inset-0 flex items-center justify-center z-20">
            <div className="bg-white w-5/12 p-8 mt-20 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold mb-4">Copy your article link</h2>
                <p>Translate any article by copying its link</p>
                <div className="flex flex-row items-center mt-3">
                    <input
                        type="text"
                        className="flex-grow px-4 py-2 border rounded-md shadow-sm focus:outline-blue-500 leading-tight"
                        placeholder="Enter something..."
                        onChange={(e) => setInputLink(e.target.value)}
                    />
                    <button onClick={() => { okButtonHandler(props) }} className="ml-4 px-4 py-2 bg-blue-500 text-white rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2">
                        OK
                    </button>
                </div>

                {/* if the link is not valid, show an error message */}
                {!isValidLink && <p className="text-red-500 text-sm mt-2">Please enter a valid link</p>}
            </div>
        </div>
    );
};

function Modal(props) {
    const closeModalHandler = () => {
        console.log('please close');
        props.onModalClose()
    }

    return ReactDOM.createPortal(
        <div>
            <Backdrop onCloseModal={closeModalHandler} />
            <ModalOverlay onModalClose={props.onModalClose} onUploadFileClose={props.onUploadFileClose} onSetArticle={props.onSetArticle} />
        </div>,
        document.getElementById('modal-root')

    );
}

export default Modal;
