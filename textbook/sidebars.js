// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['introduction/index', 'introduction/preface'],
      collapsed: false,
    },
    {
      type: 'category',
      label: '1. ROS 2',
      items: [
        'ros2/index',
        'ros2/intro-to-ros2',
        'ros2/nodes-and-topics',
        'ros2/practical-examples'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '2. Gazebo / Unity Simulation',
      items: [
        'gazebo-unity/index',
        'gazebo-unity/gazebo-basics',
        'gazebo-unity/unity-simulation',
        'gazebo-unity/comparison-study'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '3. NVIDIA Isaac Robotics',
      items: [
        'nvidia-isaac/index',
        'nvidia-isaac/isaac-sim-overview',
        'nvidia-isaac/robotics-scenarios',
        'nvidia-isaac/deployment-guide'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: '4. Vision-Language-Action (VLA) Systems',
      items: [
        'vla-systems/index',
        'vla-systems/vision-models',
        'vla-systems/language-models',
        'vla-systems/action-planning'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Conclusion',
      items: ['conclusion/index'],
      collapsed: false,
    },
  ],
};

export default sidebars;
