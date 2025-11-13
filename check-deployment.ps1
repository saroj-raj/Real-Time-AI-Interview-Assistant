# Deployment Status Checker

Write-Host "🔍 Checking Deployment Status..." -ForegroundColor Cyan
Write-Host ""

# Check if backend URL is provided
$backendUrl = Read-Host "Enter your Render backend URL (or press Enter to skip)"

if ($backendUrl) {
    Write-Host ""
    Write-Host "Testing Backend..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$backendUrl/" -Method Get -TimeoutSec 10
        Write-Host "✅ Backend is LIVE!" -ForegroundColor Green
        Write-Host "   Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
    } catch {
        Write-Host "❌ Backend not responding yet" -ForegroundColor Red
        Write-Host "   (This is normal during initial deployment)" -ForegroundColor Gray
    }
}

# Check if frontend URL is provided
$frontendUrl = Read-Host "Enter your Vercel frontend URL (or press Enter to skip)"

if ($frontendUrl) {
    Write-Host ""
    Write-Host "Testing Frontend..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri $frontendUrl -Method Get -TimeoutSec 10
        Write-Host "✅ Frontend is LIVE!" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
    } catch {
        Write-Host "❌ Frontend not responding yet" -ForegroundColor Red
        Write-Host "   (This is normal during initial deployment)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "📌 Don't forget to:" -ForegroundColor Cyan
Write-Host "   1. Update ALLOWED_ORIGINS on Render with your Vercel URL (or ALLOWED_ORIGIN_REGEX for patterns)"
Write-Host "   2. Update NEXT_PUBLIC_API_URL on Vercel with your Render URL"
Write-Host "   3. Enable Google Auth in Firebase Console"
Write-Host "   4. Add Vercel domain to Firebase authorized domains"
Write-Host "   5. Re-enter Vercel env vars without trailing spaces/newlines (especially Firebase API key and authDomain)"
Write-Host ""
Write-Host "📚 Full checklist in DEPLOYMENT.md" -ForegroundColor Gray
