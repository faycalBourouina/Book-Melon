"use client";

import React, { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const createSubmitHandler = (endpoint) => async (event) => {
    event.preventDefault();

    // Submit the email to your server for authentication
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: email })
    });

    // Update the message with the server's response
    const text = await response.text();
    setMessage(text);
  };

  return (
    <main>
      <h1>Login</h1>
      <form onSubmit={createSubmitHandler('api/login')}>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <button onClick={createSubmitHandler('api/signup')}>Sign Up</button>
      <p>{message}</p>
    </main>
  );
}
