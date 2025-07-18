import React ,{useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import Vehicles from './Vehicles';
import Bikes from './Bikes';
import About from './About';
import Contact from './Contact';

function App(){
  const [message, setMessage] = useState('');

  useEffect(()=> {
    axios.get('http://localhost:5000')
    .then(res => setMessage(res.data.message))
    .catch(err => console.log(err));


  },[]);

  return (
    <Router>
      <Navbar/>
      <P>{message}</P>

      <Routes>

        <Route path="/vehicles" element={<Vehicles/>}/>
        <Route path="/bikes" element={<Bikes/>}/>
        <Route path="/about" element={<About/>}/>
        <Route path="/contact" element={<Contact/>}/>


      </Routes>
    </Router>
    
  );

}

export default App;