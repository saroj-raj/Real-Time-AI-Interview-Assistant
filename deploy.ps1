# Quick Deployment Script for Windows

Write-Host "🚀 Starting deployment process..." -ForegroundColor Green

# Check if running in correct directory
if (-not (Test-Path "DEPLOYMENT.md")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Pre-deployment Checklist:" -ForegroundColor Cyan
Write-Host "   ✓ Groq API Key ready"
Write-Host "   ✓ Firebase project created"
Write-Host "   ✓ GitHub repository ready"
Write-Host ""

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# Add all files
Write-Host "📝 Adding files to git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m "Prepare for deployment"

# Check if remote exists
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host ""
    Write-Host "⚠️  No git remote found!" -ForegroundColor Yellow
    Write-Host "Please add your GitHub repository:"
    Write-Host ""
    $repoUrl = Read-Host "Enter your GitHub repo URL"
    git remote add origin $repoUrl
}

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Deploy Backend (Render):"
Write-Host "   → Go to: https://dashboard.render.com/create?type=web"
Write-Host "   → Connect your GitHub repo"
Write-Host "   → Set root directory: backend"
Write-Host "   → Add environment variables (see DEPLOYMENT.md)"
Write-Host ""
Write-Host "2. Deploy Frontend (Vercel):"
Write-Host "   → Go to: https://vercel.com/new"
Write-Host "   → Import your GitHub repo"
Write-Host "   → Set root directory: frontend"
Write-Host "   → Add environment variables (see DEPLOYMENT.md)"
Write-Host ""
Write-Host "📚 Full instructions: Get-Content DEPLOYMENT.md"
Write-Host ""
Write-Host "🎉 Ready to deploy!" -ForegroundColor Green
