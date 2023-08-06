
import QtQuick 1.0

Rectangle {
    id: window
    width: 480; height: 800

    property variant presenter

    Item {
        id: close_button
        width: 48; height: 48
        anchors.right: parent.right

        Rectangle {
            color: "yellow"
            anchors.fill: parent

            MouseArea {
                anchors.fill: parent
                onClicked: presenter.quit()
            }
        }
    }	  
}
