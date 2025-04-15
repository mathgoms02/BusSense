# Use an official Node.js runtime as the base image
FROM node:16

# Install Yarn globally
RUN npm install yarn

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Copy the rest of the application code to the container
COPY . .

# Expose a port (if your Node.js application needs it)
EXPOSE 3333

# Define the command to run your application
CMD ["yarn", "run", "dev"]

