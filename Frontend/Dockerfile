# Use an official Node.js image as a parent image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json to install dependencies
COPY Frontend/app/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY ./Frontend/app /app

# Expose the port the app runs on
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
