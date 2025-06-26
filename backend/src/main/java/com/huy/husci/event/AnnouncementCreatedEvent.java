package com.huy.husci.event;

import com.huy.husci.model.Announcement;

public class AnnouncementCreatedEvent {
    private final Announcement announcement;

    public AnnouncementCreatedEvent(Announcement announcement) {
        this.announcement = announcement;
    }

    public Announcement getAnnouncement() {
        return announcement;
    }
}
