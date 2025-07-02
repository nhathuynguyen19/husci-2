package com.huy.husci.utils.event;

import com.huy.husci.repository.entity.Announcement;

public class AnnouncementCreatedEvent {
    private final Announcement announcement;

    public AnnouncementCreatedEvent(Announcement announcement) {
        this.announcement = announcement;
    }

    public Announcement getAnnouncement() {
        return announcement;
    }
}
