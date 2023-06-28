"use client";
import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
      <main>
        <h1>Home</h1>
        <Link href="/authentication"> Authentication</Link>
        <Link href="/reservations"> Reservations</Link>
        <Link href="/schedule"> Schedule</Link>
      </main>
  );
}