import './index.css';

// we need useState to store the state of the modal
import { useState } from 'react';

import UploadFile from './components/UploadFile';
import Modal from './components/Modal';
import LoadingScreen from './components/LoadingScreen';

import ArticleDisplay from './components/DisplayArticle';

function App() {

  // the modal state
  const [showModal, setShowModal] = useState(false);

  // the state of UploadFile
  const [showUploadFile, setShowUploadFile] = useState(true);

  // the article with useState
  const [article, setArticle] = useState(null);


  // the function to toggle the modal
  const ModalOpenHandler = () => {
    setShowModal(true);
  };

  const ModalCloseHandler = () => {
    setShowModal(false);
  };

  // the function to toggle the UploadFile
  const UploadFileOpenHandler = () => {
    setShowUploadFile(true);
  }

  const UploadFileCloseHandler = () => {
    setShowUploadFile(false);
  }

  // the function to set the article
  const setArticleHandler = (article) => {
    setArticle(article);
  }


  return (
    <div className="bg-slate-400 h-screen">
      {article ? <ArticleDisplay article={article} /> :
        <div>
          {showUploadFile ? <UploadFile onModalOpen={ModalOpenHandler} /> : <LoadingScreen />}
          {showModal ? <Modal onModalClose={ModalCloseHandler} onUploadFileClose={UploadFileCloseHandler} onSetArticle={setArticleHandler} /> : null}
        </div>}
    </div>
  );
}

export default App;
