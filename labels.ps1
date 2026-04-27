$GitHubLabels = @(
    @{
        Name = "bug"
        Color = "b60205"
        Description = "Unexpected problem or broken behavior."
    },
    @{
        Name = "enhancement"
        Color = "a2eeef"
        Description = "New feature or improvement."
    },
    @{
        Name = "documentation"
        Color = "0075ca"
        Description = "Docs update or clarification needed."
    },
    @{
        Name = "question"
        Color = "d876e3"
        Description = "Needs more information."
    },
    @{
        Name = "help wanted"
        Color = "008672"
        Description = "Maintainer wants help on this issue."
    },
    @{
        Name = "good first issue"
        Color = "7057ff"
        Description = "Good starter task for new contributors."
    }
)

$GitHubLabels | ForEach-Object {
    [PSCustomObject]$_
} | Format-Table -AutoSize
