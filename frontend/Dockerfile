# Build stage
FROM node:latest AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json/yarn.lock
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all project files
COPY . .

# Build the application (skipping type check)
RUN npm run build-only

# Copy the built files to a location that will be accessible from outside
# This allows us to copy these files into the nginx container later
CMD ["cp", "-r", "dist/", "/output/"]
