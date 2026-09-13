import React from 'react';
import './Products.css';

const projects = [
  {
    title: 'AI Scheduler',
    description: 'Automatically schedule your tasks using GPT-4.',
    link: '#',
  },
  {
    title: 'Smart Summarizer',
    description: 'Summarize long documents in seconds.',
    link: '#',
  },
  {
    title: 'Image Enhancer',
    description: 'Enhance images with AI-powered upscaling.',
    link: '#',
  },
];

const Products = () => (
  <section className="products section">
    <h2 className="section-title">Projects</h2>
    <div className="cards">
      {projects.map((p, i) => (
        <div key={i} className="card">
          <h3 className="card-title">{p.title}</h3>
          <p className="card-desc">{p.description}</p>
          <a href={p.link} className="card-link">Learn More</a>
        </div>
      ))}
    </div>
    <div className="all-projects-link">
      <a href="/projects">View all projects -&gt;</a>
    </div>
  </section>
);

export default Products;
