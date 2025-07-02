package com.huy.husci.utils.event;

import com.huy.husci.repository.entity.Announcement;

public class AnnouncementDeletedEvent {
    private final Announcement announcement;

    public AnnouncementDeletedEvent(Announcement announcement) {
        this.announcement = announcement;
    }

    public Announcement getAnnouncement() {
        return announcement;
    }
}
