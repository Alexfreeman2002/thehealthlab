// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCEWPt2InfOjU1ZPSQ6BAgHrrv7AQVOGt8",
  authDomain: "thehealthlab.firebaseapp.com",
  projectId: "thehealthlab",
  storageBucket: "thehealthlab.appspot.com",
  messagingSenderId: "953338093921",
  appId: "1:953338093921:web:5bbd5b4a3ca213a0bd6520",
  measurementId: "G-HDVWL90PMN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);