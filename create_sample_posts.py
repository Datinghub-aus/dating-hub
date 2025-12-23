import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datinghub.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import BlogCategory, BlogPost
from django.utils import timezone
import random

# Get or create admin user
user, _ = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@datinghub.com', 'is_staff': True, 'is_superuser': True}
)

# Create categories
categories_data = [
    {'name': 'Dating Apps', 'slug': 'dating-apps'},
    {'name': 'Relationships', 'slug': 'relationships'},
    {'name': 'Online Dating', 'slug': 'online-dating'},
    {'name': 'First Dates', 'slug': 'first-dates'},
    {'name': 'Profile Tips', 'slug': 'profile-tips'},
    {'name': 'Research', 'slug': 'research'},
]

categories = {}
for cat_data in categories_data:
    cat, _ = BlogCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name']}
    )
    categories[cat.slug] = cat

# Sample blog posts with Unsplash images
blog_posts = [
    {
        'title': 'The Rise of Video Dating: How Apps Are Adapting',
        'slug': 'rise-of-video-dating',
        'category': categories['dating-apps'],
        'excerpt': 'Explore how dating apps are integrating video features and what it means for users.',
        'content': '''<h2>The Video Dating Revolution</h2>
<p>In the post-pandemic world, video dating has moved from a niche feature to a mainstream expectation. Apps that were once solely focused on text and photos are now racing to add video capabilities.</p>

<h3>Why Video Matters</h3>
<p>Video calls reduce catfishing, build better connections before meeting in person, and save time. Our research shows that users who video chat before meeting are 40% more likely to have successful first dates.</p>

<h3>Platforms Leading the Way</h3>
<ul>
<li><strong>Hinge:</strong> Introduced video prompts in profiles</li>
<li><strong>Bumble:</strong> Has built-in video calling</li>
<li><strong>Tinder:</strong> Testing video profiles in select markets</li>
</ul>

<p>The future of dating is moving toward more authentic, real-time connections through video integration.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Person video calling on a dating app',
        'read_time': 5,
        'meta_title': 'Video Dating Trends 2026',
        'meta_description': 'How dating apps are adapting to video features and what it means for users'
    },
    {
        'title': '2026 Dating App Success Rates by Age Group',
        'slug': '2026-dating-app-success-rates',
        'category': categories['research'],
        'excerpt': 'New research reveals which dating apps work best for different age demographics.',
        'content': '''<h2>Age-Specific Dating Success</h2>
<p>Our latest study of 10,000 users reveals significant differences in app success rates across age groups.</p>

<h3>Key Findings</h3>
<table>
<tr><th>Age Group</th><th>Most Successful App</th><th>Success Rate</th></tr>
<tr><td>18-24</td><td>Tinder</td><td>72%</td></tr>
<tr><td>25-34</td><td>Hinge</td><td>68%</td></tr>
<tr><td>35-44</td><td>Bumble</td><td>65%</td></tr>
<tr><td>45+</td><td>eHarmony</td><td>71%</td></tr>
</table>

<h3>What This Means for You</h3>
<p>Choosing the right platform for your age group can significantly improve your dating experience. Younger users prefer fast-paced, visual apps, while older users value detailed profiles and compatibility algorithms.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Statistical data on a screen',
        'read_time': 7,
        'meta_title': 'Dating App Success Rates by Age',
        'meta_description': 'Research on which dating apps work best for different age groups in 2026'
    },
    {
        'title': 'Creating a Winning Dating Profile: 2026 Edition',
        'slug': 'winning-dating-profile-2026',
        'category': categories['profile-tips'],
        'excerpt': 'Updated tips for creating a profile that stands out in the current dating landscape.',
        'content': '''<h2>Profile Optimization for 2026</h2>
<p>With algorithm changes and new user expectations, here are the updated best practices for dating profiles.</p>

<h3>Photo Strategy</h3>
<p>Include these 5 essential photos:</p>
<ol>
<li>Clear face shot (smiling!)</li>
<li>Full body shot in casual clothes</li>
<li>Activity/hobby photo</li>
<li>Social photo (with friends)</li>
<li>Pet photo (if you have one)</li>
</ol>

<h3>Bio Writing Tips</h3>
<ul>
<li>Keep it under 150 characters</li>
<li>Include specific interests</li>
<li>Use humor when appropriate</li>
<li>Mention what you\'re looking for</li>
</ul>

<h3>Prompt Responses</h3>
<p>Most apps now include prompts. Be authentic, specific, and positive in your responses.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Person creating a dating profile on phone',
        'read_time': 6,
        'meta_title': 'How to Create a Winning Dating Profile',
        'meta_description': 'Updated tips for creating standout dating profiles in 2026'
    },
    {
        'title': 'The Psychology of First Messages That Get Replies',
        'slug': 'psychology-first-messages',
        'category': categories['online-dating'],
        'excerpt': 'Research-backed strategies for crafting opening messages that actually get responses.',
        'content': '''<h2>The Science of First Messages</h2>
<p>Our analysis of 50,000 first messages reveals what works and what doesn\'t.</p>

<h3>What Works</h3>
<ul>
<li><strong>Reference their profile:</strong> 3x more likely to get a reply</li>
<li><strong>Ask open-ended questions:</strong> 2.5x more engagement</li>
<li><strong>Use humor appropriately:</strong> 2x higher response rate</li>
<li><strong>Keep it short (1-2 sentences):</strong> Optimal length</li>
</ul>

<h3>What Doesn\'t Work</h3>
<ul>
<li>"Hey" or "Hi" (12% response rate)</li>
<li>Generic compliments (18% response rate)</li>
<li>Overly long messages (22% response rate)</li>
<li>Immediate requests for dates (15% response rate)</li>
</ul>

<h3>Examples of Great First Messages</h3>
<p>"I see you\'re into hiking - have you tried the [local trail] trail?"</p>
<p>"Your dog in the third photo is adorable! What breed is it?"</p>''',
        'image_url': 'https://images.unsplash.com/photo-1587560699334-cc4ff634909a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Person typing a message on phone',
        'read_time': 8,
        'meta_title': 'Psychology of Effective First Messages',
        'meta_description': 'Research-backed strategies for dating app first messages that get replies'
    },
    {
        'title': 'Niche Dating Apps: Finding Your Perfect Community',
        'slug': 'niche-dating-apps-guide',
        'category': categories['dating-apps'],
        'excerpt': 'Specialized dating apps for every interest, lifestyle, and community.',
        'content': '''<h2>Beyond the Mainstream Apps</h2>
<p>While Tinder and Bumble dominate, niche apps offer specialized experiences for specific communities.</p>

<h3>By Interest</h3>
<ul>
<li><strong>Feeld:</strong> For open-minded and polyamorous dating</li>
<li><strong>Farmers Only:</strong> For rural singles and farmers</li>
<li><strong>Tastebuds:</strong> Matches based on music taste</li>
</ul>

<h3>By Lifestyle</h3>
<ul>
<li><strong>Raya:</strong> Exclusive app for creatives</li>
<li><strong>Bristlr:</strong> For beard lovers</li>
<li><strong>Gluten Free Singles:</strong> For dietary-specific dating</li>
</ul>

<h3>By Religion</h3>
<ul>
<li><strong>JDate:</strong> Jewish dating</li>
<li><strong>Christian Mingle:</strong> Christian dating</li>
<li><strong>Muzmatch:</strong> Muslim dating</li>
</ul>

<p>Niche apps often have higher success rates for their target demographics.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Various dating app icons on a screen',
        'read_time': 6,
        'meta_title': 'Guide to Niche Dating Apps',
        'meta_description': 'Specialized dating apps for every interest and community'
    },
    {
        'title': 'Safety First: Protecting Yourself in Online Dating',
        'slug': 'online-dating-safety-guide',
        'category': categories['online-dating'],
        'excerpt': 'Essential safety tips for protecting yourself while dating online.',
        'content': '''<h2>Staying Safe in Digital Dating</h2>
<p>Protect yourself with these essential safety practices.</p>

<h3>Before Meeting</h3>
<ul>
<li>Video chat first</li>
<li>Verify social media profiles</li>
<li>Google their name and phone number</li>
<li>Tell a friend about your plans</li>
</ul>

<h3>First Date Safety</h3>
<ul>
<li>Meet in public places</li>
<li>Arrange your own transportation</li>
<li>Keep alcohol consumption minimal</li>
<li>Have an exit strategy</li>
</ul>

<h3>Digital Safety</h3>
<ul>
<li>Don\'t share personal information too quickly</li>
<li>Use the app\'s messaging system initially</li>
<li>Be cautious with location sharing</li>
<li>Trust your instincts</li>
</ul>

<p>Remember: It\'s always okay to cancel or leave if you feel uncomfortable.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Person being safe while using dating app',
        'read_time': 5,
        'meta_title': 'Online Dating Safety Guide',
        'meta_description': 'Essential safety tips for protecting yourself while dating online'
    },
    {
        'title': 'The Impact of AI on Modern Matchmaking',
        'slug': 'ai-modern-matchmaking',
        'category': categories['research'],
        'excerpt': 'How artificial intelligence is revolutionizing how we find love online.',
        'content': '''<h2>AI: The New Matchmaker</h2>
<p>Artificial intelligence is transforming dating apps from simple swipe platforms to sophisticated matchmakers.</p>

<h3>How AI Improves Matching</h3>
<ul>
<li><strong>Behavioral Analysis:</strong> Learns from your swipes and conversations</li>
<li><strong>Image Verification:</strong> Detects fake or misleading photos</li>
<li><strong>Conversation Analysis:</strong> Suggests responses and topics</li>
<li><strong>Compatibility Prediction:</strong> Uses machine learning to predict successful matches</li>
</ul>

<h3>Current AI Features</h3>
<p>Leading apps now use AI for:</p>
<ul>
<li>Photo selection optimization</li>
<li>Profile completion suggestions</li>
<li>Match quality scoring</li>
<li>Safety feature enhancements</li>
</ul>

<h3>The Future of AI Dating</h3>
<p>Expect more personalized experiences, better fraud detection, and enhanced compatibility algorithms.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'AI and machine learning concepts',
        'read_time': 7,
        'meta_title': 'AI in Modern Dating Apps',
        'meta_description': 'How artificial intelligence is revolutionizing online matchmaking'
    },
    {
        'title': 'Long-Distance Dating in the Digital Age',
        'slug': 'long-distance-digital-dating',
        'category': categories['relationships'],
        'excerpt': 'Making long-distance relationships work with modern technology.',
        'content': '''<h2>Love Across Distances</h2>
<p>Technology has made long-distance relationships more feasible than ever before.</p>

<h3>Essential Tools</h3>
<ul>
<li><strong>Video Calls:</strong> Daily face-to-face connection</li>
<li><strong>Shared Activities:</strong> Watch parties, online games</li>
<li><strong>Messaging Apps:</strong> Constant communication</li>
<li><strong>Date Planning Apps:</strong> Coordinate visits and activities</li>
</ul>

<h3>Success Strategies</h3>
<ul>
<li>Schedule regular video dates</li>
<li>Set clear communication expectations</li>
<li>Plan the next visit during the current one</li>
<li>Develop shared interests and hobbies</li>
</ul>

<h3>When to Consider Long-Distance</h3>
<p>Long-distance works best when there\'s an end date in sight and both partners are committed to making it work.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Couple video calling long distance',
        'read_time': 6,
        'meta_title': 'Long-Distance Dating Guide',
        'meta_description': 'Making long-distance relationships work with modern technology'
    },
    {
        'title': 'Dating After Divorce: A Modern Guide',
        'slug': 'dating-after-divorce-guide',
        'category': categories['relationships'],
        'excerpt': 'Navigating the dating world after a divorce or long-term relationship.',
        'content': '''<h2>Starting Over</h2>
<p>Re-entering the dating world after divorce comes with unique challenges and opportunities.</p>

<h3>Preparing Yourself</h3>
<ul>
<li>Take time to heal</li>
<li>Reflect on what you want</li>
<li>Update your wardrobe and photos</li>
<li>Practice talking about your past</li>
</ul>

<h3>Choosing the Right Platform</h3>
<p>Different apps cater to different life stages:</p>
<ul>
<li><strong>eHarmony:</strong> Serious relationships, older demographic</li>
<li><strong>Match:</strong> Broad user base, various ages</li>
<li><strong>OurTime:</strong> Specifically for 50+</li>
</ul>

<h3>Navigating Conversations</h3>
<p>Be honest but brief about your past. Focus on the present and future rather than dwelling on the divorce.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Mature person using dating app',
        'read_time': 8,
        'meta_title': 'Dating After Divorce Guide',
        'meta_description': 'Navigating modern dating after divorce or long-term relationships'
    },
    {
        'title': 'The Economics of Dating Apps: Who\'s Making Money?',
        'slug': 'economics-dating-apps',
        'category': categories['research'],
        'excerpt': 'Understanding the business models behind popular dating platforms.',
        'content': '''<h2>The Business of Love</h2>
<p>Dating apps have become billion-dollar businesses. Here\'s how they make money.</p>

<h3>Revenue Models</h3>
<ul>
<li><strong>Subscription Tiers:</strong> Premium features at monthly rates</li>
<li><strong>In-App Purchases:</strong> Boosts, super likes, coins</li>
<li><strong>Advertising:</strong> Display ads and sponsored profiles</li>
<li><strong>Data Monetization:</strong> Anonymized user data for research</li>
</ul>

<h3>Average User Spending</h3>
<p>Our research shows average monthly spending:</p>
<ul>
<li>Tinder Gold: $29.99/month</li>
<li>Bumble Premium: $24.99/month</li>
<li>Hinge Preferred: $29.99/month</li>
<li>eHarmony: $59.95/month</li>
</ul>

<h3>Market Share 2026</h3>
<p>Match Group (Tinder, Hinge, Match) controls 65% of the market, followed by Bumble at 25%.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Financial charts and data',
        'read_time': 7,
        'meta_title': 'Economics of Dating Apps',
        'meta_description': 'Understanding the business models behind popular dating platforms'
    },
    {
        'title': 'First Date Ideas That Actually Work',
        'slug': 'first-date-ideas-guide',
        'category': categories['first-dates'],
        'excerpt': 'Creative and effective first date ideas for memorable experiences.',
        'content': '''<h2>Beyond Coffee and Drinks</h2>
<p>Stand out with these creative first date ideas that encourage connection.</p>

<h3>Low-Pressure Options</h3>
<ul>
<li><strong>Museum Visit:</strong> Conversation starters everywhere</li>
<li><strong>Walk in the Park:</strong> Casual, public, no time pressure</li>
<li><strong>Bookstore Browsing:</strong> Learn about each other\'s interests</li>
<li><strong>Food Truck Festival:</strong> Variety and casual atmosphere</li>
</ul>

<h3>Activity-Based Dates</h3>
<ul>
<li><strong>Mini Golf:</strong> Playful and fun</li>
<li><strong>Cooking Class:</strong> Collaborative experience</li>
<li><strong>Arcade Games:</strong> Nostalgic and entertaining</li>
<li><strong>Pottery Painting:</strong> Creative and relaxed</li>
</ul>

<h3>What to Avoid</h3>
<ul>
<li>Movies (no talking)</li>
<li>Expensive restaurants (pressure)</li>
<li>Your home or theirs (safety)</li>
<li>Group dates initially (distracting)</li>
</ul>''',
        'image_url': 'https://images.unsplash.com/photo-1518568814500-bf0f8d125f46?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Couple on a creative first date',
        'read_time': 6,
        'meta_title': 'Creative First Date Ideas',
        'meta_description': 'Effective first date ideas for memorable experiences'
    },
    {
        'title': 'Mental Health and Dating Apps: Finding Balance',
        'slug': 'mental-health-dating-apps',
        'category': categories['relationships'],
        'excerpt': 'How to use dating apps without compromising your mental wellbeing.',
        'content': '''<h2>Healthy Dating App Habits</h2>
<p>Protect your mental health while navigating the world of online dating.</p>

<h3>Recognizing Negative Patterns</h3>
<ul>
<li>Constantly checking for matches</li>
<li>Taking rejections personally</li>
<li>Comparing yourself to others</li>
<li>Feeling addicted to swiping</li>
</ul>

<h3>Healthy Usage Tips</h3>
<ul>
<li>Set time limits (30 minutes/day)</li>
<li>Take regular breaks (1 week/month)</li>
<li>Focus on quality over quantity</li>
<li>Remember it\'s just one way to meet people</li>
</ul>

<h3>When to Take a Break</h3>
<p>Signs you need a dating app detox:</p>
<ul>
<li>Feeling anxious about checking the app</li>
<li>Negative self-talk after rejections</li>
<li>Dating app fatigue</li>
<li>Impact on sleep or work</li>
</ul>

<p>Your mental health should always come first.</p>''',
        'image_url': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'image_alt': 'Person practicing self-care while using phone',
        'read_time': 7,
        'meta_title': 'Dating Apps and Mental Health',
        'meta_description': 'How to use dating apps without compromising mental wellbeing'
    }
]

# Create blog posts
for i, post_data in enumerate(blog_posts):
    post, created = BlogPost.objects.get_or_create(
        slug=post_data['slug'],
        defaults={
            'title': post_data['title'],
            'author': user,
            'category': post_data['category'],
            'excerpt': post_data['excerpt'],
            'content': post_data['content'],
            'image_url': post_data['image_url'],
            'image_alt': post_data['image_alt'],
            'read_time': post_data['read_time'],
            'status': 'published',
            'published_at': timezone.now(),
            'meta_title': post_data.get('meta_title', ''),
            'meta_description': post_data.get('meta_description', '')
        }
    )
    if created:
        print(f"Created: {post.title}")
    else:
        print(f"Exists: {post.title}")

print(f"\nCreated {len(blog_posts)} sample blog posts!")
