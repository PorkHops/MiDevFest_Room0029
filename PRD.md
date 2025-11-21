# Product Requirements Document (PRD)  
**Event Lite**  
**“Your Personal Local Event Curator Powered by watsonx”**

| Item                  | Details |
|-----------------------|------------------------------------------------------------|
| Product Name          | Event Lite |
| Version               | 1.0 (MVP) |
| Date                  | November 21, 2025 |
| Target Launch         | Q1 2026 |
| Primary Goal          | Deliver a hyper-personalized, real-time local event discovery experience using conversational AI (IBM watsonx Agent) with zero manual searching. |

### 1. Vision & Value Proposition
**One-sentence vision:**  
Event Lite is the simplest way to always know what’s happening locally that you’ll actually enjoy — by chatting naturally with an AI that remembers your tastes.

**Core Value Props:**
- Zero event-search fatigue  
- Always up-to-date (real-time scraping + official APIs)  
- Truly personalized via ongoing conversation  
- Beautiful daily view (“What’s happening today/tomorrow?”)  
- Works on mobile & desktop

### 2. Target Users
- Urban, suburban, and rural professionals 22–45  
- People who feel FOMO but hate browsing Eventbrite, Facebook Events, Meetup, etc.  
- Frequent concert/festival goers, foodies, art lovers, runners, parents, gamers, etc.

### 3. Key Features (MVP)

| Priority | Feature | Description |
|---------|-------|-----------|
| 1 | Location Detection & Permission | Auto-detect or manually set city/metro area (with radius selector: 5–50 mi/km) |
| 2 | Daily Event Timeline (Home Screen) | Clean, scrollable view grouped by day (“Today”, “Tomorrow”, “This Weekend”, “Next 7 Days”) with event cards (image, title, venue, time, price, short AI summary) |
| 3 | Embedded watsonx Agent Chat | Full-screen or floating chat widget powered by IBM watsonx.ai Agent that can: <br>• Understand natural language interests <br>• Ask clarifying questions <br>• Remember preferences across sessions (persisted per user) <br>• Trigger real-time event search & ranking |
| 4 | Real-time Preference Sync | When user chats (“I love jazz and outdoor markets”, “No kids events”, “Under $30”), the home timeline instantly re-ranks/refreshes without page reload |
| 5 | Event Sources (Real-time) | watsonx Agent orchestrates calls to: <br>• Eventbrite API <br>• Ticketmaster Discovery API <br>• Meetup API <br>• Google Places + local venue calendars (via scraping tools in watsonx) <br>• Local news & city calendar RSS when needed |
| 6 | Save / “Interested” + Calendar Export | One-tap ❤️ to save event → adds to personal list + optional .ics export or Google Calendar add |
| 7 | User Accounts (Lightweight) | Email + magic link or OAuth (Google/Apple) for persistence of preferences & saved events |
| 8 | Responsive Web App (PWA) | Installable on home screen, works offline for cached events |

### 4. User Flow (Core Loop)
1. User lands → grants location → sees today’s personalized events  
2. Opens chat → “Hey, I’m into techno and vegan food this month”  
3. watsonx Agent confirms: “Got it! Looking for techno parties and vegan-friendly events within 20 miles. Any price limit?”  
4. User: “Under $40, and nothing before 7pm”  
5. Agent instantly updates the main timeline with newly ranked events + highlights new additions  
6. User taps ❤️ on two events → they appear in “My Events” tab  
7. Background: preferences are saved permanently to user profile

### 5. Technical Architecture

```
Frontend (React + Vite + TypeScript)
├── Tailwind CSS + shadcn/ui components
├── TanStack Query for data fetching
├── Socket.io / SSE for real-time updates from backend
├── PWA manifest & service worker

Backend (Python Flask)
├── Flask + Flask-SQLAlchemy (PostgreSQL)
├── Flask-Login (magic links)
├── Flask-SocketIO for real-time chat & timeline push
├── Celery + Redis for background scraping jobs
├── Rate limiting & caching (Redis)

IBM watsonx.ai Integration
├── watsonx Agentic Orchestrator (custom agent built in watsonx.ai)
├── Tools exposed to agent:
    - search_eventbrite(query, location, date_range, price_max)
    - search_ticketmaster(...)
    - search_meetup(...)
    - scrape_venue_calendar(url)
    - get_user_preferences(user_id)
    - save_user_preferences(user_id, json)
├── Agent uses ReAct + function calling pattern
├── All calls go through secure backend proxy (never expose API keys to frontend)

Deployment
├── Backend: Render.com / Fly.io / AWS ECS
├── Frontend: Vercel / Netlify
├── Database: Supabase Postgres or AWS RDS
├── watsonx: IBM Cloud (GenAI tier)
```

### 6. Non-functional Requirements
- < 2s initial load with cached events  
- Real-time chat response < 3s  
- 99.5% uptime  
- GDPR/CCPA compliant (explicit consent for location & preferences)  
- Accessible (WCAG 2.1 AA)

### 7. Success Metrics (First 90 Days)
- 10,000 monthly active users  
- Average 4.2+ chat sessions per user per week  
- 65% of users save at least one event in first session  
- >50% week-1 retention

### 8. Future Roadmap (Post-MVP)
- Group plans (“Create plan with friends”)  
- Ticket purchasing in-app  
- AI-generated event summaries & “why you’ll love this”  
- Spotify/Instagram interest import  
- Push notifications (“Your favorite DJ just announced a pop-up tonight”)  
- Mobile native apps (React Native)

### 9. Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Event API rate limits | Aggressive caching + fallback to scraping tools inside watsonx |
| Location privacy concerns | Explicit permission + on-device first load possible |
| watsonx cost overruns | Token monitoring + fallback to lighter LLM for simple queries |
| Event data quality | Human-in-the-loop curation for top cities in v1.1 |

**Tagline:**  
“Stop searching for plans. Start having them.”

Prepared for immediate development — MVP achievable in 10–12 weeks with a team of 1 full-stack + 1 AI engineer + 1 designer.

Let’s go build Event Lite.
