// firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";

// TODO: Replace with your Firebase project configuration
// 1. Go to Firebase Console (https://console.firebase.google.com/)
// 2. Create a new project (it's free)
// 3. Register a Web App and copy the config object below
const firebaseConfig = {
  projectId: "krishikarm-2a047",
  appId: "1:932121564110:web:300476bc401ab4adc1919f",
  storageBucket: "krishikarm-2a047.firebasestorage.app",
  apiKey: "AIzaSyDL3AKQ6m7W0tqUtTya-mOAEikCUT0mO80",
  authDomain: "krishikarm-2a047.firebaseapp.com",
  messagingSenderId: "932121564110",
  measurementId: "G-RM9Y5JVNTB",
  projectNumber: "932121564110"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const db = getFirestore(app);
export const auth = getAuth(app);
