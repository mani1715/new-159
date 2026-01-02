import React from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink, Github, Star } from 'lucide-react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import './portfolio-components.css';

const ProjectCard = ({ project }) => {
  if (!project) return null;

  const {
    id,
    title,
    slug,
    category,
    description,
    image_url,
    tech_stack = [],
    featured,
    live_demo_url,
    github_url,
  } = project;

  return (
    <Card className="project-card-premium" data-admin-editable={`project-${id}`}>
      {/* Featured Badge */}
      {featured && (
        <div className="project-featured-badge">
          <Star className="h-3 w-3" fill="currentColor" />
          <span>Featured</span>
        </div>
      )}

      {/* Image */}
      <div className="project-card-image-wrapper">
        <img
          src={image_url}
          alt={title}
          className="project-card-image"
          loading="lazy"
          decoding="async"
        />

        {/* Hover Overlay */}
        <div className="project-card-overlay">
          <div className="project-overlay-buttons">
            <Link to={`/portfolio/${slug || id}`}>
              <Button className="project-overlay-btn btn-view">
                View Case Study
              </Button>
            </Link>

            {live_demo_url && (
              <a
                href={live_demo_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button className="project-overlay-btn btn-demo">
                  <ExternalLink className="h-4 w-4" />
                  Live Demo
                </Button>
              </a>
            )}
          </div>
        </div>

        {/* Category */}
        <div className="project-category-badge">{category}</div>
      </div>

      {/* Content */}
      <div className="project-card-content">
        <h3 className="project-card-title">{title}</h3>
        <p className="project-card-description">{description}</p>

        {/* Tech Stack */}
        <div className="project-tech-tags">
          {tech_stack.slice(0, 4).map((tech, idx) => (
            <span key={idx} className="tech-tag">
              {tech}
            </span>
          ))}
          {tech_stack.length > 4 && (
            <span className="tech-tag tech-tag-more">
              +{tech_stack.length - 4}
            </span>
          )}
        </div>

        {/* Footer */}
        <div className="project-card-footer">
          <Link
            to={`/portfolio/${slug || id}`}
            className="project-read-more"
          >
            View Details →
          </Link>

          {github_url && (
            <a
              href={github_url}
              target="_blank"
              rel="noopener noreferrer"
              className="project-github-link"
            >
              <Github className="h-4 w-4" />
            </a>
          )}
        </div>
      </div>

      <div className="project-card-gradient"></div>
    </Card>
  );
};

export default ProjectCard;
