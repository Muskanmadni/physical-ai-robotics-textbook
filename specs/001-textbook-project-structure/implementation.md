---

description: "Implementation blueprint for Physical AI & Humanoid Robotics textbook project"
---

# Implementation Blueprint: Physical AI & Humanoid Robotics Textbook

**Feature**: textbook-project-structure  
**Date**: 2025-12-05  
**Input**: 
- specs/001-textbook-project-structure/spec.md
- specs/001-textbook-project-structure/plan.md  
- specs/001-textbook-project-structure/tasks.md

## 1. REPO STRUCTURE (Docusaurus v3)

### Complete Folder Tree
```
physical-ai-humanoid-robotics-textbook/          # Main textbook project
├── textbook/                                   # Docusaurus frontend
│   ├── docs/                                   # Textbook chapters
│   │   ├── intro/
│   │   │   ├── index.md
│   │   │   └── preface.md
│   │   ├── modules/
│   │   │   ├── ros2/
│   │   │   │   ├── index.md
│   │   │   │   ├── intro-to-ros2.md
│   │   │   │   ├── nodes-and-topics.md
│   │   │   │   └── practical-examples.md
│   │   │   ├── gazebo-unity/
│   │   │   │   ├── index.md
│   │   │   │   ├── gazebo-basics.md
│   │   │   │   ├── unity-simulation.md
│   │   │   │   └── comparison-study.md
│   │   │   ├── nvidia-isaac/
│   │   │   │   ├── index.md
│   │   │   │   ├── isaac-sim-overview.md
│   │   │   │   ├── robotics-scenarios.md
│   │   │   │   └── deployment-guide.md
│   │   │   └── vla-systems/
│   │   │       ├── index.md
│   │   │       ├── vision-models.md
│   │   │       ├── language-models.md
│   │   │       └── action-planning.md
│   │   └── conclusion/
│   │       ├── summary.md
│   │       └── future-directions.md
│   ├── src/
│   │   ├── components/
│   │   │   ├── PersonalizationToggle/
│   │   │   ├── TranslationToggle/
│   │   │   ├── ProgressTracker/
│   │   │   └── RAGSearch/
│   │   ├── pages/
│   │   │   ├── index.js
│   │   │   ├── auth/
│   │   │   │   ├── login.js
│   │   │   │   └── register.js
│   │   │   └── dashboard/
│   │   │       └── index.js
│   │   └── css/
│   │       └── custom.css
│   ├── static/
│   │   ├── img/
│   │   │   ├── logo.svg
│   │   │   └── hero-image.png
│   │   └── files/
│   ├── .github/
│   │   └── workflows/
│   │       └── deploy.yml
│   ├── babel.config.js
│   ├── docusaurus.config.js
│   ├── package.json
│   ├── postcss.config.js
│   ├── sidebars.js
│   └── README.md
├── rag-backend/                                # FastAPI backend
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── chapter.py
│   │   │   ├── module.py
│   │   │   ├── user_progress.py
│   │   │   ├── quiz.py
│   │   │   ├── quiz_submission.py
│   │   │   ├── rag_document.py
│   │   │   ├── personalized_content.py
│   │   │   └── translation.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── content_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── personalization_service.py
│   │   │   └── translation_service.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── content.py
│   │   │   ├── search.py
│   │   │   ├── quizzes.py
│   │   │   ├── progress.py
│   │   │   ├── rag.py
│   │   │   ├── personalization.py
│   │   │   └── translation.py
│   │   └── utils/
│   │       ├── embeddings.py
│   │       ├── database.py
│   │       └── middleware.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_content.py
│   │   ├── test_rag.py
│   │   └── test_personalization.py
│   ├── requirements.txt
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── .env.example
│   └── README.md
├── specs/                                      # Project specifications
│   └── 001-textbook-project-structure/         # Current feature specs
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       ├── tasks.md
│       ├── implementation.md
│       └── contracts/
│           └── api-contracts.md
├── assets/
│   ├── images/
│   ├── videos/
│   └── diagrams/
├── .gitignore
├── .env
├── LICENSE
└── README.md
```

### All Files (Even Empty Ones)
- Empty placeholder files created for each module/chapter to maintain structure
- Configuration files with default settings that match requirements
- Documentation files with placeholder content that follows Docusaurus format

## 2. DOCUSAURUS IMPLEMENTATION

### docusaurus.config.js
```javascript
// Docusaurus configuration for Physical AI & Humanoid Robotics textbook
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Comprehensive Educational Resource',
  url: 'https://your-username.github.io',
  baseUrl: '/physical-ai-humanoid-robotics-textbook/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-username', // Usually your GitHub org/user name.
  projectName: 'physical-ai-humanoid-robotics-textbook', // Usually your repo name.
  trailingSlash: false,

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/physical-ai-humanoid-robotics-textbook/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Textbook Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Textbook',
          },
          { to: '/auth', label: 'Auth', position: 'right' },
          { to: '/dashboard', label: 'Dashboard', position: 'right' },
          {
            href: 'https://github.com/your-username/physical-ai-humanoid-robotics-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'ROS 2',
                to: '/docs/modules/ros2/',
              },
              {
                label: 'Gazebo/Unity',
                to: '/docs/modules/gazebo-unity/',
              },
              {
                label: 'NVIDIA Isaac',
                to: '/docs/modules/nvidia-isaac/',
              },
              {
                label: 'VLA Systems',
                to: '/docs/modules/vla-systems/',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Licensed under MIT.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/github'),
        darkTheme: require('prism-react-renderer/themes/dracula'),
      },
    }),
  
  plugins: [
    // Plugin for RAG search functionality
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'rag-search',
        path: 'docs',
        routeBasePath: 'rag-search',
      },
    ],
  ],
};
```

### sidebars.js
```javascript
// Sidebar configuration for textbook navigation
// Generated based on modules structure in plan.md

module.exports = {
  textbook: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro/index', 'intro/preface'],
      collapsed: false,
    },
    {
      type: 'category',
      label: '1. ROS 2',
      items: [
        'modules/ros2/index',
        'modules/ros2/intro-to-ros2',
        'modules/ros2/nodes-and-topics',
        'modules/ros2/practical-examples'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '2. Gazebo / Unity Simulation',
      items: [
        'modules/gazebo-unity/index',
        'modules/gazebo-unity/gazebo-basics',
        'modules/gazebo-unity/unity-simulation',
        'modules/gazebo-unity/comparison-study'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '3. NVIDIA Isaac Robotics',
      items: [
        'modules/nvidia-isaac/index',
        'modules/nvidia-isaac/isaac-sim-overview',
        'modules/nvidia-isaac/robotics-scenarios',
        'modules/nvidia-isaac/deployment-guide'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '4. Vision-Language-Action (VLA) Systems',
      items: [
        'modules/vla-systems/index',
        'modules/vla-systems/vision-models',
        'modules/vla-systems/language-models',
        'modules/vla-systems/action-planning'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Conclusion',
      items: ['conclusion/summary', 'conclusion/future-directions'],
      collapsed: false,
    },
  ],
};
```

### Routing for Chapters
- Each module and chapter has its own route based on the folder structure
- Custom MDX components for interactive elements
- Search functionality integrated with RAG backend

### Versions and Docs Categories
- Versioning setup to support future editions of the textbook
- Multiple document categories for different content types (theory, practice, examples)

### Navbar/Footer Plan
- Navigation optimized for textbook structure
- Footer with quick links to important sections
- Auth and dashboard links for personalized experience

## 3. CONTENT PIPELINE

### How Chapters are Generated
1. Content is written in Markdown format following Docusaurus standards
2. Each chapter includes code snippets, diagrams, and references
3. Chapters are organized by module in the docs/ directory
4. Cross-references between chapters use Docusaurus's link system
5. Build process transforms Markdown to optimized web pages

### How Code Blocks, Diagrams, Images are Handled
- Code blocks use Docusaurus's built-in syntax highlighting
- Diagrams can be included as static images or generated with Mermaid
- Images are optimized during build process
- Custom React components for interactive diagrams

### Multi-Module → Multi-Chapter Mapping
- 4 major modules as defined in plan.md
- Each module contains 3-4 chapters with detailed content
- Navigation organized hierarchically by module then chapter
- Cross-module references where appropriate

### Claude/Qwen-assisted Content Workflow
- Agent integration for content generation and refinement
- Subagents for specific tasks (code-gen, diagrams, chapter refinement)
- Content review and validation pipeline

## 4. RAG BACKEND BLUEPRINT

### FastAPI Service Structure
```
rag-backend/
├── src/
│   ├── main.py                 # Application entry point
│   ├── models/                 # Pydantic models and database models
│   │   ├── user.py            # User model
│   │   ├── chapter.py         # Chapter model
│   │   ├── rag_document.py    # RAG document model
│   │   └── ...
│   ├── services/              # Business logic layer
│   │   ├── rag_service.py     # RAG-related operations
│   │   ├── auth_service.py    # Authentication operations
│   │   └── ...
│   ├── api/                   # API routes
│   │   ├── rag.py             # RAG endpoints
│   │   ├── auth.py            # Auth endpoints
│   │   └── ...
│   └── utils/                 # Utilities
│       ├── embeddings.py      # Embedding operations
│       └── ...
```

### Embedding Pipeline
1. Textbook content is processed and chunked into manageable pieces
2. Embeddings are generated using a suitable model (e.g., sentence-transformers)
3. Embeddings are stored in Qdrant vector database
4. Metadata is stored in Neon PostgreSQL database
5. New content updates trigger incremental embedding updates

### Qdrant Schema
- Collection for textbook content chunks
- Vector size configured for the embedding model used
- Payload includes document metadata (chapter ID, module, etc.)
- Support for filtering by chapter/module during search

### Neon Database
- User accounts and profiles
- Chapter and module metadata
- User progress tracking
- Quiz questions and submissions
- Personalized content references

### Client Fetch Hooks
- Docusaurus components use API endpoints to fetch personalized content
- Search functionality connects to RAG endpoint
- Authentication state managed through cookies or tokens

### Personalization Logic
- User preferences stored in database
- Content adaptation based on user interactions
- Machine learning model to recommend next chapters or content

## 5. FRONTEND FEATURES

### Auth Placeholder
- Login and registration pages using Better-Auth
- Protected routes for personalized content
- User dashboard to view progress and preferences

### Personalization Placeholder
- Toggle buttons for personalized content per chapter
- Custom content rendering based on user profile
- Progress tracking and recommendations

### Urdu Translation Toggle
- Language switching functionality
- Content translated and stored in separate documents
- RTL text support for Urdu

### Chapter Progress Tracking
- Progress saved automatically as user reads
- Progress indicators in sidebar
- Next chapter recommendations

## 6. AGENT INTEGRATION

### Subagents for Specific Tasks
1. **Code-gen Subagent**: Generates and validates code examples
2. **Diagrams Subagent**: Creates visual representations of concepts
3. **Chapter Refinement Subagent**: Improves existing content quality

### Prompt Boundaries
- Clearly defined input/output formats for each agent
- Quality validation steps after agent processing
- Human review checkpoints

### Clear Chaining Steps
1. Content draft created
2. Agent processes specific aspects (code, diagrams, etc.)
3. Output validated and refined
4. Integrated into textbook structure

## 7. PHASED EXECUTION

### Phase 1: Project Setup
- [ ] Create repository structure
- [ ] Initialize Docusaurus project
- [ ] Set up GitHub Pages workflow
- [ ] Create basic configuration files
- [ ] Set up license and documentation

### Phase 2: Content Framework
- [ ] Create all module and chapter files with placeholders
- [ ] Configure navigation and sidebars
- [ ] Set up basic styling with WCAG compliance
- [ ] Implement content template structure

### Phase 3: RAG + Bonus Features
- [ ] Set up FastAPI backend
- [ ] Implement RAG functionality with Neon and Qdrant
- [ ] Add authentication system
- [ ] Implement personalization features
- [ ] Add translation functionality

### Phase 4: Testing + Deployment
- [ ] Run RAG accuracy tests (target: 90%+ on 20 queries)
- [ ] Perform accessibility checks for WCAG compliance
- [ ] Deploy to GitHub Pages
- [ ] Conduct human review checkpoint

## 8. ACCEPTANCE CRITERIA

### Docusaurus Frontend
- **Definition of Done**: All textbook content is accessible through properly structured navigation
- **Expected Artifacts**: Complete Docusaurus site with all modules/chapters
- **Validation**: Site builds without errors, all links work, navigation is intuitive

### RAG Backend
- **Definition of Done**: RAG queries return relevant results with 90%+ accuracy
- **Expected Artifacts**: FastAPI server with RAG endpoints, connected to Neon and Qdrant
- **Validation**: Test queries return accurate textbook-related information

### Authentication System
- **Definition of Done**: Users can register, login, and access personalized features
- **Expected Artifacts**: Working auth endpoints and UI components
- **Validation**: Successful registration, login, and access to user-specific features

### Translation Feature
- **Definition of Done**: Content can be switched between English and Urdu
- **Expected Artifacts**: Translation toggle and Urdu content
- **Validation**: Content displays correctly in both languages

### Deployment
- **Definition of Done**: Site is accessible via GitHub Pages
- **Expected Artifacts**: Deployed site at configured URL
- **Validation**: All functionality works in production environment

## 9. DEPLOYMENT PLAN

### GitHub Pages Workflow
- Workflow automatically triggers on pushes to main branch
- Builds the Docusaurus site using Node.js environment
- Deploys static files to GitHub Pages
- Includes environment-specific configurations

### Build Steps
1. Install Node.js dependencies
2. Build Docusaurus site with `npm run build`
3. Deploy static files to GitHub Pages
4. Verify deployment success

### Environment Variable Handling
- Environment-specific configurations in .env files
- Secure handling of API keys and secrets
- Different configurations for development and production
- Configuration validation during build process