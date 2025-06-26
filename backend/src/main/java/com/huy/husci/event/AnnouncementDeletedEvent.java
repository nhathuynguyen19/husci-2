package com.huy.husci.event;

import com.huy.husci.model.Announcement;

public class AnnouncementDeletedEvent {
    private final Announcement announcement;

    public AnnouncementDeletedEvent(Announcement announcement) {
        this.announcement = announcement;
    }

    public Announcement getAnnouncement() {
        return announcement;
    }
}
