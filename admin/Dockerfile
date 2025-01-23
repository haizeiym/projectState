# Use the official Node.js image as the base image
FROM node:18-alpine AS build-stage

# Set the working directory
WORKDIR /app

# Set environment variable
ARG NODE_ENV
ENV NODE_ENV=${NODE_ENV}

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Use Nginx to serve the application
FROM nginx:stable-alpine AS production-stage

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build output to Nginx's html directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 