import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Mail,
  Database,
  MessageSquare,
  Users,
  StickyNote,
  Settings,
  Sparkles,
  BookOpen,
  Briefcase,
  Monitor,
  FileText,
  X,
  Pen,
  MessageCircle,
  Newspaper,
  Calculator,
  BarChart3,
  UserCog,
  FolderKanban,
  Calendar,
  Clock
} from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const navItems = [
    { path: '/admin/about', icon: BookOpen, label: 'About' },
    { path: '/admin/portfolio', icon: Briefcase, label: 'Portfolio' },
    { path: '/admin/blogs', icon: Pen, label: 'Blogs' },
    { path: '/admin/testimonials', icon: MessageCircle, label: 'Testimonials' },
    { path: '/admin/demos', icon: Monitor, label: 'Demos' },
    { path: '/admin/contacts', icon: Mail, label: 'Contacts' },
    { path: '/admin/contact-page', icon: FileText, label: 'Contact Page' },
    { path: '/admin/bookings', icon: Calendar, label: 'Bookings' },
    { path: '/admin/booking-settings', icon: Clock, label: 'Booking Settings' },
    { path: '/admin/newsletter', icon: Newspaper, label: 'Newsletter' },
    { path: '/admin/pricing', icon: Calculator, label: 'Pricing Calculator' },
    { path: '/admin/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/admin/clients', icon: UserCog, label: 'Clients' },
    { path: '/admin/client-projects', icon: FolderKanban, label: 'Client Projects' },
    { path: '/admin/storage', icon: Database, label: 'Storage' },
    { path: '/admin/chat', icon: MessageSquare, label: 'Chat' },
    { path: '/admin/notes', icon: StickyNote, label: 'Notes' },
    { path: '/admin/admins', icon: Users, label: 'Admins' },
    { path: '/admin/settings', icon: Settings, label: 'Settings' },
  ];

  const handleNavClick = () => {
    // Close sidebar on mobile when a link is clicked
    if (window.innerWidth <= 768 && onClose) {
      onClose();
    }
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="admin-sidebar-overlay" 
          onClick={onClose}
        />
      )}
      
      <aside className={`admin-sidebar ${isOpen ? 'open' : ''}`}>
        <div className="admin-sidebar-header">
          <a href="/admin/contacts" className="admin-logo">
            <div className="admin-logo-icon">
              <Sparkles size={24} />
            </div>
            <span>MSPN DEV</span>
          </a>
          
          {/* Mobile Close Button */}
          <button 
            className="admin-sidebar-close"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <X size={24} />
          </button>
        </div>
        
        <nav className="admin-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => 
                `admin-nav-item ${isActive ? 'active' : ''}`
              }
              onClick={handleNavClick}
            >
              <item.icon className="admin-nav-icon" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;
