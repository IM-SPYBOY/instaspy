import os
import sys
import time
import random
import json
import requests
import re
import argparse
import datetime
from termcolor import colored
from instagrapi import Client
from googlesearch import search
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Detect operating system
IS_WINDOWS = os.name == 'nt'
IS_LINUX = os.name == 'posix'

# Clear screen function
def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')

# Display banner (your original art preserved)
def show_banner():
    clear_screen()
    print(colored("""                                                                         
@@@  @@@  @@@   @@@@@@   @@@@@@@   @@@@@@    @@@@@@   @@@@@@@   @@@ @@@  
@@@  @@@@ @@@  @@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@@  @@@ @@@  
@@!  @@!@!@@@  !@@         @@!    @@!  @@@  !@@       @@!  @@@  @@! !@@  
!@!  !@!!@!@!  !@!         !@!    !@!  @!@  !@!       !@!  @!@  !@! @!!  
!!@  @!@ !!@!  !!@@!!      @!!    @!@!@!@!  !!@@!!    @!@@!@!    !@!@!   
!!!  !@!  !!!   !!@!!!     !!!    !!!@!!!!   !!@!!!   !!@!!!      @!!!   
!!:  !!:  !!!       !:!    !!:    !!:  !!!       !:!  !!:         !!:    
:!:  :!:  !:!      !:!     :!:    :!:  !:!      !:!   :!:         :!:    
 ::   ::   ::  :::: ::      ::    ::   :::  :::: ::    ::          ::    
:    ::    :   :: : :       :      :   : :  :: : :     :           :     
                                                                         
                       InstaSpy v1.0  
""", 'cyan'))
    print(f"{Fore.YELLOW}Platform: {sys.platform}")
    print(f"{Fore.GREEN}Python: {sys.version.split()[0]}\n")
    print(f"{Fore.MAGENTA}Developed for OSINT professionals | No limits | Real-time output\n")

# Configuration
SESSION_FILE = 'session.json'

def save_session(client):
    """Save session data to file"""
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(client.get_settings(), f)
        print(f"{Fore.GREEN}✓ Session saved successfully")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Error saving session: {e}")
        return False

def load_session(client):
    """Load session data from file"""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                client.set_settings(json.load(f))
            print(f"{Fore.GREEN}✓ Session restored from file")
            return True
    except Exception as e:
        print(f"{Fore.RED}✗ Error loading session: {e}")
    return False

def get_user_info(client, username):
    """Get user info with modern API method"""
    try:
        print(f"{Fore.CYAN}[•] Fetching user ID for @{username}...")
        user_id = client.user_id_from_username(username)
        print(f"{Fore.GREEN}✓ User ID found: {user_id}")
        
        print(f"{Fore.CYAN}[•] Retrieving user information...")
        user = client.user_info(user_id)
        print(f"{Fore.GREEN}✓ User info retrieved successfully")
        return user
    except Exception as e:
        print(f"{Fore.RED}✗ Error getting user info: {e}")
        return None

# ==================== USER INFORMATION ====================
def fetch_user_information(client, username):
    """Fetch comprehensive user information including contact details"""
    try:
        # API URL for contact information lookup
        api_url = ''.join([chr(int(x, 16)) for x in ['68','74','74','70','73','3A','2F','2F','69','2E','69','6E','73','74','61','67','72','61','6D','2E','63','6F','6D','2F','61','70','69','2F','76','31','2F','75','73','65','72','73','2F','6C','6F','6F','6B','75','70','2F']])
        
        print(f"\n{Fore.CYAN}➤ Fetching comprehensive information for @{username}...")
        user = get_user_info(client, username)
        if not user:
            return

        # Fetch contact information
        headers = {
            'accept-language': 'en-US;q=1.0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Instagram 337.0.3.23.54 (iPhone12,1; iOS 16_6; en_US; en; scale=2.00; 828x1792; 577210397) AppleWebKit/420+',
        }
        data = {"q": username}
        
        try:
            response = requests.post(api_url, headers=headers, data=data)
            response.raise_for_status()
            contact_data = response.json()
            phone = contact_data.get('phone_number', 'Not available')
            email = contact_data.get('email', 'Not available')
        except:
            phone = 'Not available'
            email = 'Not available'

        # Display user information
        print(f"\n{Fore.MAGENTA}★ User Information ★")
        print(f"{Fore.CYAN}Username: {Fore.WHITE}{user.username}")
        print(f"{Fore.CYAN}Full Name: {Fore.WHITE}{user.full_name}")
        print(f"{Fore.CYAN}User ID: {Fore.WHITE}{user.pk}")
        print(f"{Fore.CYAN}Bio: {Fore.WHITE}{user.biography}")
        print(f"{Fore.CYAN}External URL: {Fore.WHITE}{user.external_url}")
        print(f"{Fore.CYAN}Private Account: {Fore.WHITE}{'Yes' if user.is_private else 'No'}")
        print(f"{Fore.CYAN}Business Account: {Fore.WHITE}{'Yes' if user.is_business else 'No'}")
        print(f"{Fore.CYAN}Phone Number: {Fore.WHITE}{phone}")
        print(f"{Fore.CYAN}Email: {Fore.WHITE}{email}")
        print(f"{Fore.CYAN}Followers: {Fore.WHITE}{user.follower_count}")
        print(f"{Fore.CYAN}Following: {Fore.WHITE}{user.following_count}")
        print(f"{Fore.CYAN}Posts: {Fore.WHITE}{user.media_count}")
        
        # Save to file
        filename = f"{username}_information.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"User Information for @{username}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Username: {user.username}\n")
            f.write(f"Full Name: {user.full_name}\n")
            f.write(f"User ID: {user.pk}\n")
            f.write(f"Bio: {user.biography}\n")
            f.write(f"External URL: {user.external_url}\n")
            f.write(f"Private Account: {'Yes' if user.is_private else 'No'}\n")
            f.write(f"Business Account: {'Yes' if user.is_business else 'No'}\n")
            f.write(f"Phone Number: {phone}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Followers: {user.follower_count}\n")
            f.write(f"Following: {user.following_count}\n")
            f.write(f"Posts: {user.media_count}\n")
        
        print(f"\n{Fore.GREEN}✓ Information saved to {filename}")
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error fetching user information: {e}")
# ==================== END USER INFORMATION ====================

# ==================== POST DOWNLOAD ====================
def download_user_posts(client, username):
    """Download all posts of the target Instagram user"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        if user.is_private:
            print(f"{Fore.YELLOW}Account is private. Checking if followed...")
            following = client.user_following(client.user_id)
            if user.pk not in following:
                print(f"{Fore.RED}✗ You don't follow this private account")
                return

        print(f"{Fore.CYAN}➤ Downloading posts for @{username}...")
        posts = client.user_medias(user.pk, amount=0)
        
        if not posts:
            print(f"{Fore.YELLOW}No posts found")
            return
            
        folder = f"{username}_posts"
        os.makedirs(folder, exist_ok=True)
        print(f"{Fore.GREEN}✓ Downloading {len(posts)} posts to {folder}/")
        
        for idx, post in enumerate(posts, 1):
            try:
                # Determine media type and URL
                if post.media_type == 1:  # Photo
                    url = post.thumbnail_url
                    ext = "jpg"
                elif post.media_type == 2:  # Video
                    url = post.video_url
                    ext = "mp4"
                else:  # Carousel
                    url = post.thumbnail_url
                    ext = "jpg"
                
                filename = f"{folder}/post_{idx}.{ext}"
                
                # Download media
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"{Fore.GREEN}✓ Downloaded post {idx}/{len(posts)}")
                time.sleep(1)  # Avoid rate limiting
                
            except Exception as e:
                print(f"{Fore.RED}✗ Error downloading post {idx}: {e}")
        
        print(f"{Fore.MAGENTA}✓ All posts downloaded to {folder}/")

    except Exception as e:
        print(f"{Fore.RED}✗ Error downloading posts: {e}")
# ==================== END POST DOWNLOAD ====================

# ==================== STORY DOWNLOAD ====================
def download_stories(client, username):
    """Download user stories"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        if user.is_private:
            print(f"{Fore.YELLOW}Account is private. Checking if followed...")
            following = client.user_following(client.user_id)
            if user.pk not in following:
                print(f"{Fore.RED}✗ You don't follow this private account")
                return

        print(f"{Fore.CYAN}➤ Downloading stories for @{username}...")
        stories = client.user_stories(user.pk)
        
        if not stories:
            print(f"{Fore.YELLOW}No stories available")
            return
            
        folder = f"{username}_stories"
        os.makedirs(folder, exist_ok=True)
        print(f"{Fore.GREEN}✓ Downloading {len(stories)} stories to {folder}/")
        
        for idx, story in enumerate(stories, 1):
            try:
                # Determine media type and URL
                if story.media_type == 1:  # Photo
                    url = story.thumbnail_url
                    ext = "jpg"
                else:  # Video
                    url = story.video_url
                    ext = "mp4"
                
                filename = f"{folder}/story_{idx}.{ext}"
                
                # Download media
                response = requests.get(url)
                response.raise_for_status()
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"{Fore.GREEN}✓ Downloaded story {idx}/{len(stories)}")
                time.sleep(1)  # Avoid rate limiting
                
            except Exception as e:
                print(f"{Fore.RED}✗ Error downloading story {idx}: {e}")
        
        print(f"{Fore.MAGENTA}✓ All stories downloaded to {folder}/")

    except Exception as e:
        print(f"{Fore.RED}✗ Error downloading stories: {e}")
# ==================== END STORY DOWNLOAD ====================

# ==================== HIGHLIGHT DOWNLOAD ====================
def download_highlights(client, username):
    """Download user highlights"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        if user.is_private:
            print(f"{Fore.YELLOW}Account is private. Checking if followed...")
            following = client.user_following(client.user_id)
            if user.pk not in following:
                print(f"{Fore.RED}✗ You don't follow this private account")
                return

        print(f"{Fore.CYAN}➤ Downloading highlights for @{username}...")
        highlights = client.user_highlights(user.pk)
        
        if not highlights:
            print(f"{Fore.YELLOW}No highlights available")
            return
            
        base_dir = f"{username}_highlights"
        os.makedirs(base_dir, exist_ok=True)
        print(f"{Fore.GREEN}✓ Downloading {len(highlights)} highlights to {base_dir}/")
        
        for highlight in highlights:
            try:
                highlight_info = client.highlight_info(highlight.pk)
                highlight_folder = os.path.join(base_dir, highlight.title)
                os.makedirs(highlight_folder, exist_ok=True)
                
                for idx, item in enumerate(highlight_info.items, 1):
                    try:
                        media_url = item.video_url or item.thumbnail_url
                        ext = "mp4" if item.video_url else "jpg"
                        filename = os.path.join(highlight_folder, f"highlight_{idx}.{ext}")
                        
                        response = requests.get(media_url, stream=True)
                        response.raise_for_status()
                        
                        with open(filename, "wb") as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        
                        print(f"{Fore.GREEN}✓ Downloaded {highlight.title} highlight {idx}")
                        time.sleep(1)
                    except Exception as e:
                        print(f"{Fore.RED}✗ Error downloading highlight {idx}: {e}")
            except Exception as e:
                print(f"{Fore.RED}✗ Error processing highlight: {e}")
        
        print(f"{Fore.MAGENTA}✓ All highlights downloaded to {base_dir}/")

    except Exception as e:
        print(f"{Fore.RED}✗ Error downloading highlights: {e}")
# ==================== END HIGHLIGHT DOWNLOAD ====================

# ==================== GOOGLE DORK SEARCH ====================
def collect_google_dork_data(username):
    """Unlimited Google dork search with real-time output"""
    try:
        print(f"\n{Fore.CYAN}➤ Starting unlimited Google dork search for @{username}...")
        query = f'site:instagram.com intext:{username}'
        results = []
        
        print(f"{Fore.YELLOW}⚡ Search query: {query}")
        print(f"{Fore.YELLOW}⚠ This may take several minutes. Press Ctrl+C to stop early.\n")

        try:
            # Start unlimited search
            for idx, url in enumerate(search(query, num=100, stop=None, pause=5), 1):
                results.append(url)
                print(f"{Fore.GREEN}[{idx}] {url}")
                
                # Save progress every 10 results
                if idx % 10 == 0:
                    with open(f"{username}_dork_results.txt", 'w', encoding='utf-8') as f:
                        f.write("\n".join(results))
                    print(f"{Fore.YELLOW}⚡ Saved {idx} results so far...")
                
                # Random delay to avoid blocking (1-5 seconds)
                delay = random.uniform(1, 5)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}⚠ Search interrupted by user")
        except Exception as e:
            print(f"{Fore.RED}✗ Search error: {e}")

        # Final save
        results_file = f"{username}_dork_results.txt"
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(f"Google Dork Results for @{username}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Search Query: {query}\n")
            f.write(f"Total Results: {len(results)}\n\n")
            f.write("\n".join(results))

        print(f"\n{Fore.MAGENTA}★ Search Complete ★")
        print(f"{Fore.CYAN}→ Total results collected: {len(results)}")
        print(f"{Fore.CYAN}→ Results saved to: {results_file}")

    except Exception as e:
        print(f"{Fore.RED}✗ Fatal error during search: {e}")
# ==================== END GOOGLE DORK SEARCH ====================

# ==================== COMMENT COLLECTION ====================
def collect_comments(client, username):
    """Collect comments from all posts"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        print(f"{Fore.CYAN}➤ Collecting comments for @{username}...")
        posts = client.user_medias(user.pk, amount=0)
        
        if not posts:
            print(f"{Fore.YELLOW}No posts found")
            return
            
        comments_file = f"{username}_comments.txt"
        comment_count = 0
        
        with open(comments_file, 'w', encoding='utf-8') as f:
            f.write(f"Comments for @{username}\n")
            f.write("=" * 50 + "\n\n")
            
            for post_idx, post in enumerate(posts, 1):
                try:
                    comments = client.media_comments(post.pk)
                    if not comments:
                        continue
                        
                    f.write(f"Post {post_idx} ({post.pk}):\n")
                    for comment in comments:
                        f.write(f"  {comment.user.username}: {comment.text}\n")
                        comment_count += 1
                    f.write("\n")
                    
                    print(f"{Fore.GREEN}✓ Collected {len(comments)} comments from post {post_idx}")
                    
                except Exception as e:
                    print(f"{Fore.RED}✗ Error getting comments for post {post_idx}: {e}")
        
        print(f"{Fore.MAGENTA}✓ Total comments collected: {comment_count}")
        print(f"{Fore.MAGENTA}✓ Comments saved to: {comments_file}")

    except Exception as e:
        print(f"{Fore.RED}✗ Error collecting comments: {e}")
# ==================== END COMMENT COLLECTION ====================

# ==================== GEO DATA COLLECTION ====================
def collect_geo_data(client, username):
    """Collect geographical data from user posts"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        print(f"{Fore.CYAN}➤ Collecting geo data for @{username}...")
        posts = client.user_medias(user.pk, amount=20)
        
        if not posts:
            print(f"{Fore.YELLOW}No posts found")
            return
            
        locations = []
        for post in posts:
            try:
                if post.location:
                    location = post.location
                    locations.append({
                        'post_id': post.pk,
                        'name': location.name,
                        'lat': location.lat,
                        'lng': location.lng
                    })
                    print(f"{Fore.GREEN}✓ Found location: {location.name}")
            except:
                continue
        
        if not locations:
            print(f"{Fore.YELLOW}No location data found")
            return
            
        filename = f"{username}_geo_data.json"
        with open(filename, 'w') as f:
            json.dump(locations, f, indent=2)
            
        print(f"{Fore.MAGENTA}✓ Saved {len(locations)} locations to {filename}")

    except Exception as e:
        print(f"{Fore.RED}✗ Error collecting geo data: {e}")
# ==================== END GEO DATA COLLECTION ====================

# ==================== FOLLOWER/FOLLOWING COLLECTION ====================
def print_followers_and_following(client, username):
    """Get all followers/following without limits and display in real-time"""
    try:
        user = get_user_info(client, username)
        if not user:
            return

        print(f"\n{Fore.CYAN}➤ Collecting ALL followers for @{username}...")
        followers = client.user_followers(user.pk)
        print(f"{Fore.GREEN}✓ Total followers found: {len(followers)}")
        
        # Save followers to file and display in real-time
        followers_file = f"{username}_followers.txt"
        with open(followers_file, 'w', encoding='utf-8') as f:
            f.write(f"Followers of @{username} ({len(followers)}):\n\n")
            for idx, (pk, user) in enumerate(followers.items(), 1):
                f.write(f"{idx}. {user.username}\n")
                # Display every 10th follower to avoid flooding the terminal
                if idx % 10 == 0 or idx == len(followers):
                    print(f"{Fore.GREEN}✓ Collected {idx}/{len(followers)} followers: {user.username}")
        
        print(f"{Fore.MAGENTA}✓ Followers saved to: {followers_file}")

        print(f"\n{Fore.CYAN}➤ Collecting ALL following for @{username}...")
        following = client.user_following(user.pk)
        print(f"{Fore.GREEN}✓ Total following found: {len(following)}")
        
        # Save following to file and display in real-time
        following_file = f"{username}_following.txt"
        with open(following_file, 'w', encoding='utf-8') as f:
            f.write(f"Following by @{username} ({len(following)}):\n\n")
            for idx, (pk, user) in enumerate(following.items(), 1):
                f.write(f"{idx}. {user.username}\n")
                # Display every 10th following to avoid flooding the terminal
                if idx % 10 == 0 or idx == len(following):
                    print(f"{Fore.GREEN}✓ Collected {idx}/{len(following)} following: {user.username}")
        
        print(f"{Fore.MAGENTA}✓ Following saved to: {following_file}")

        print(f"\n{Fore.YELLOW}★ Collection Complete ★")
        print(f"{Fore.CYAN}→ Followers: {len(followers)}")
        print(f"{Fore.CYAN}→ Following: {len(following)}")
        print(f"{Fore.CYAN}→ Files saved: {followers_file}, {following_file}")

    except Exception as e:
        print(f"{Fore.RED}✗ Fatal error during collection: {e}")
# ==================== END FOLLOWER/FOLLOWING COLLECTION ====================

from colorama import Fore, Style

def display_menu():
    """Show interactive menu"""
    print(f"\n{Fore.CYAN}┌{'─' * 60}┐")
    print(f"│{Fore.MAGENTA} INSTASPY MENU {Fore.CYAN}{' ' * 45}│")
    print(f"├{'─' * 60}┤")
    print(f"│ {Fore.GREEN}1. Fetch User Information                      │")
    print(f"│ {Fore.GREEN}2. Download User Posts                         │")
    print(f"│ {Fore.GREEN}3. Download User Stories                       │")
    print(f"│ {Fore.GREEN}4. Download User Highlights                    │")
    print(f"│ {Fore.GREEN}5. Google Dork Search                          │")
    print(f"│ {Fore.GREEN}6. Collect Post Comments                       │")
    print(f"│ {Fore.GREEN}7. Collect Geo Data                            │")
    print(f"│ {Fore.GREEN}8. Get Followers/Following                     │")
    print(f"│ {Fore.GREEN}9. Exit                                        │")
    print(f"└{'─' * 60}┘")
    return input(f"{Fore.YELLOW}Select option (1-9): {Style.RESET_ALL}")

def main():
    """Main program flow"""
    # Initialize Instagram client
    client = Client()
    client.delay_range = [1, 3]  # Safer request intervals
    
    # Show banner
    show_banner()
    
    # Session handling
    if not load_session(client):
        print(f"\n{Fore.CYAN}➤ Login required to access Instagram API")
        username = input(f"{Fore.GREEN}Enter your Instagram username: {Style.RESET_ALL}")
        password = input(f"{Fore.GREEN}Enter your Instagram password: {Style.RESET_ALL}")
        
        try:
            print(f"{Fore.CYAN}[•] Attempting login...")
            client.login(username, password)
            print(f"{Fore.GREEN}✓ Login successful")
            save_session(client)
        except Exception as e:
            print(f"{Fore.RED}✗ Login failed: {e}")
            return
    
    # Get target username
    target = input(f"\n{Fore.CYAN}➤ Enter target Instagram username: {Style.RESET_ALL}")
    
    # Main loop
    while True:
        choice = display_menu()
        
        if choice == '1':
            print(f"\n{Fore.MAGENTA}★ Fetching information for @{target} ★")
            fetch_user_information(client, target)
        elif choice == '2':
            print(f"\n{Fore.MAGENTA}★ Downloading posts for @{target} ★")
            download_user_posts(client, target)
        elif choice == '3':
            print(f"\n{Fore.MAGENTA}★ Downloading stories for @{target} ★")
            download_stories(client, target)
        elif choice == '4':
            print(f"\n{Fore.MAGENTA}★ Downloading highlights for @{target} ★")
            download_highlights(client, target)
        elif choice == '5':
            print(f"\n{Fore.MAGENTA}★ Starting Google dork search for @{target} ★")
            collect_google_dork_data(target)
        elif choice == '6':
            print(f"\n{Fore.MAGENTA}★ Collecting comments for @{target} ★")
            collect_comments(client, target)
        elif choice == '7':
            print(f"\n{Fore.MAGENTA}★ Collecting geo data for @{target} ★")
            collect_geo_data(client, target)
        elif choice == '8':
            print(f"\n{Fore.MAGENTA}★ Collecting followers/following for @{target} ★")
            print_followers_and_following(client, target)
        elif choice == '9':
            print(f"\n{Fore.GREEN}✓ Thank you for using InstaSpy. Goodbye!")
            break
        else:
            print(f"{Fore.RED}✗ Invalid option. Please select 1-10.")
        
        # Pause before showing menu again
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...")
        show_banner()

if __name__ == "__main__":
    main()