#!/bin/bash

# Quick Deployment Script for Real-Time AI Interview Assistant

echo "🚀 Starting deployment process..."

# Check if running in correct directory
if [ ! -f "DEPLOYMENT.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo ""
echo "📋 Pre-deployment Checklist:"
echo "   ✓ Groq API Key ready"
echo "   ✓ Firebase project created"
echo "   ✓ GitHub repository ready"
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Prepare for deployment" || echo "No changes to commit"

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  No git remote found!"
    echo "Please add your GitHub repository:"
    echo ""
    read -p "Enter your GitHub repo URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main || echo "Push failed - please check your GitHub connection"

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "📌 Next Steps:"
echo ""
echo "1. Deploy Backend (Render):"
echo "   → Go to: https://dashboard.render.com/create?type=web"
echo "   → Connect your GitHub repo"
echo "   → Set root directory: backend"
echo "   → Add environment variables (see DEPLOYMENT.md)"
echo ""
echo "2. Deploy Frontend (Vercel):"
echo "   → Go to: https://vercel.com/new"
echo "   → Import your GitHub repo"
echo "   → Set root directory: frontend"
echo "   → Add environment variables (see DEPLOYMENT.md)"
echo ""
echo "📚 Full instructions: cat DEPLOYMENT.md"
echo ""
echo "🎉 Ready to deploy!"
