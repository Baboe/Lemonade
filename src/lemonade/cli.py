"""CLI entrypoint for Lemonade."""

import click
from rich.console import Console
from rich.table import Table

from lemonade import __version__
from lemonade.config import (
    QUEUE_ROOT,
    QUEUE_FOLDERS,
    ensure_queue_folders_exist,
    count_product_folders,
)

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="lemonade")
def main():
    """Lemonade - Etsy listing draft generator and browser automation tool."""
    pass


@main.group()
def etsy():
    """Etsy listing commands."""
    pass


@etsy.command()
def status():
    """Show queue folder counts.
    
    Displays the number of product folders in each queue folder:
    INBOX, READY, TODAY, DRAFTED, PUBLISHED.
    
    Creates missing queue folders automatically.
    """
    console.print(f"\n[bold]Queue Root:[/bold] {QUEUE_ROOT}\n")
    
    # Ensure all folders exist
    try:
        ensure_queue_folders_exist()
    except OSError as e:
        console.print(f"[red]ERROR:[/red] Failed to create queue folders: {e}")
        raise SystemExit(1)
    
    # Build status table
    table = Table(title="Queue Status")
    table.add_column("Folder", style="cyan", no_wrap=True)
    table.add_column("Count", justify="right", style="green")
    table.add_column("Path", style="dim")
    
    total = 0
    for folder in QUEUE_FOLDERS:
        try:
            count = count_product_folders(folder)
            total += count
            path = QUEUE_ROOT / folder
            table.add_row(folder, str(count), str(path))
        except FileNotFoundError as e:
            console.print(f"[red]ERROR:[/red] {e}")
            raise SystemExit(1)
    
    console.print(table)
    console.print(f"\n[bold]Total product folders:[/bold] {total}\n")


@etsy.command()
def prep():
    """Process INBOX folders and generate listing drafts to READY.
    
    Requires OpenAI API key in OPENAI_API_KEY environment variable.
    """
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will process INBOX and generate drafts to READY.")
    raise SystemExit(1)


@etsy.command()
def today():
    """Move next READY item to TODAY and display listing.
    
    Does not require OpenAI or browser.
    """
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will move next READY item to TODAY.")
    raise SystemExit(1)


@etsy.command(name="dry-run")
def dry_run():
    """Show what would be uploaded without browser automation.
    
    Displays all fields that would be filled in Etsy.
    """
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will show what would be uploaded.")
    raise SystemExit(1)


@etsy.command()
def draft():
    """Create Etsy draft listing via browser automation.
    
    Requires Playwright and a logged-in Etsy session.
    NEVER publishes - saves as DRAFT only.
    """
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will create an Etsy draft via browser.")
    raise SystemExit(1)


@etsy.command()
def pause():
    """Open browser and stop before Save Draft.
    
    Allows manual inspection before saving.
    """
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will pause before Save Draft.")
    raise SystemExit(1)


@etsy.command()
def screenshots():
    """View saved screenshots from browser automation."""
    console.print("[yellow]Not implemented yet.[/yellow]")
    console.print("This command will show saved screenshots.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
