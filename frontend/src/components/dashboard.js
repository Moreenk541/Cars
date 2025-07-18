
import React ,{useState} from "react";
import axios from "axios"
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

function navbar(){
    


    return (


            <motion.nav
                initial={{ y: -50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
                style={{ padding: '1rem', backgroundColor: '#f4f4f4' }} 
            >
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <Link to ="\vehicles"> Vehicles</Link>
                    <Link to="\bikes">Bikes</Link>
                    <Link to="\about">About</Link> 
                    <Link to="contact-us">Contact us</Link>

                </div>

            </motion.nav>
    )
}


export default navbar
