# Build stage
FROM nginx:stable-alpine
# FROM node:18-alpine AS build-stage

# # Set the working directory
# WORKDIR /app

# # Set environment variables
# ARG NODE_ENV
# ENV NODE_ENV=${NODE_ENV}
# ENV ROLLUP_SKIP_NODE_RESOLUTION=true
# ENV npm_config_arch=x64
# ENV npm_config_platform=linux
# ENV npm_config_target_arch=x64
# ENV npm_config_target_platform=linux

# Install dependencies first (for better caching)
# COPY package*.json ./
COPY dist ./dist
# RUN rm -rf node_modules package-lock.json
# RUN npm cache clean --force
# RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application with specific platform
# RUN npm run build

# Production stage


# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build output to Nginx's html directory
# COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 