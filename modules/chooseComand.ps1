Write-Host "Select a command to execute:"
Write-Host "1. vagrant up"
Write-Host "2. kubectl port-forward svc/postgres 5432:5432"
Write-Host "3. vagrant halt"
Write-Host "4. Build and run Docker image"
Write-Host "5. Clean up Docker system"

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    1 {
        Set-Location -Path "C:\Users\Coding4Kids\udacity-training\cd0309-message-passing-projects-starter"
        vagrant up
        Start-Sleep -Seconds 5  # kleine Pause, damit Vagrant sauber hochkommt
        kubectl port-forward svc/postgres 5432:5432
    }
    2 {
        kubectl port-forward svc/postgres 5432:5432
    }
    3 {
        Set-Location -Path "C:\Users\Coding4Kids\udacity-training\cd0309-message-passing-projects-starter"
        vagrant up
    }
    4 {
        Set-Location -Path "C:\Users\Coding4Kids\udacity-training\mb-message-passing\modules\api-locations"
        docker build -t test
        docker run -p 5002:5002 -p 5005:5005 - test
    }
    5 {
        docker system prune -af
    }
    default {
        Write-Host "Invalid choice."
    }
}

Pause