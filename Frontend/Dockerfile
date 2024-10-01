# Use the official Node.js image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY ./Frontend/app/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code to the working directory in the container
COPY ./Frontend/app .

# Expose port 3000 to the host
EXPOSE 3000

# Run the Vite development server with host 0.0.0.0 to expose it on all network interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
