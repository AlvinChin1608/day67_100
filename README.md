# day67_100
# Flask Blog App Enhancements: Improving Functionality and User Experience
This Flask web application serves as a blog platform, allowing users to create, edit, and delete blog posts. Recent enhancements have focused on improving user experience and functionality.

## Key Enhancements:
- __Modularized Design:__ Implemented {% include %} statements for a consistent header and footer, simplifying updates and maintaining a uniform design.
- __Dynamic Content Rendering:__ Used Flask's url_for function to ensure correct linking of static files and routes.
- __Bootstrap Integration:__ Enhanced the visual styling and responsiveness of the application by integrating Bootstrap. Fixed issues related to loading Bootstrap CSS and JavaScript.

  ![](https://github.com/AlvinChin1608/day67_100/blob/main/demo-gif/pagination-ezgif.com-video-to-gif-converter.gif)
  
- __Pagination:__ Added pagination to handle a large number of blog posts, improving user experience for navigating through entries.
- __CRUD Functionalities:__
    - Create, Read, Update, and Delete Functionalities
      ### Create
    ![](https://github.com/AlvinChin1608/day67_100/blob/main/demo-gif/create-ezgif.com-video-to-gif-converter.gif)
    - __Create:__ Implemented a form for users to add new blog posts with validation and saving to the database.
    - __Edit:__ Developed functionality to modify existing blog posts, allowing users to update post details.
      
      ### Delete
      ![](https://github.com/AlvinChin1608/day67_100/blob/main/demo-gif/delete-ezgif.com-video-to-gif-converter.gif)
    - __Delete:__ Added a feature to remove blog posts from the database, providing users with control over their content.
    - __Debugging:__ Addressed issues related to file paths and template inheritance.
