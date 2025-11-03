$(document).ready(function () {
  const $chatBox = $("#chat-canvas-body");

  // --- Eel Exposed Functions ---
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
      $(".siri-message li:first").text(message);
      $(".siri-message").textillate("start");
  }

  eel.expose(ShowHood);
  function ShowHood() {
      $("#Oval").attr("hidden", false);
      $("#SiriWave").attr("hidden", true);
  }

  eel.expose(senderText);
  function senderText(message) {
      appendChatMessage(message, true); 
  }

  eel.expose(receiverText);
  function receiverText(message) {
      appendChatMessage(message, false); 
  }
  
  eel.expose(hideLoader);
  function hideLoader() {
      $("#Loader").attr("hidden", true);
      $("#FaceAuth").attr("hidden", false);
  }

  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
      $("#FaceAuth").attr("hidden", true);
      $("#FaceAuthSuccess").attr("hidden", false);
  }
  
  eel.expose(showFaceAuth);
  function showFaceAuth() {
      $("#FaceAuth").attr("hidden", false);
      $("#FaceAuthSuccess").attr("hidden", true);
  }

  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
      $("#FaceAuthSuccess").attr("hidden", true);
      $("#HelloGreet").attr("hidden", false);
  }

  eel.expose(hideStart);
  function hideStart() {
      $("#Start").attr("hidden", true);

      setTimeout(function () {
          $("#Oval").addClass("animate__animated animate__zoomIn");
      }, 1000);

      setTimeout(function () {
          $("#Oval").attr("hidden", false);
      }, 1000);
  }

  function appendChatMessage(message, isSender) {
      if (!message || !message.trim()) return;

      const justifyClass = isSender ? "justify-content-end" : "justify-content-start";
      const messageClass = isSender ? "sender_message" : "receiver_message";

      $chatBox.append(`
          <div class="row ${justifyClass} mb-4">
              <div class="width-size">
                  <div class="${messageClass}">${message}</div>
              </div>
          </div>
      `);

      $chatBox.scrollTop($chatBox[0].scrollHeight);
  }

  // --- UI INTERACTION LOGIC ---
  function sendMessage() {
      const message = $("#message_input").val().trim();
      if (message) {
          eel.takeAllCommands(message)(function(response) {
              // Keep the callback to handle the return and prevent KeyError
          });
          $("#message_input").val(''); 
      }
  }

  $("#send_button").on('click', sendMessage);

  $("#message_input").keypress(function (e) {
      if (e.which === 13) {
          sendMessage();
      }
  });

  // --- INITIALIZATION ---
  // Critical: Call the Python initialization function. The callback helps fix the KeyError.
  eel.init()(function(response) {
      // Keep the callback
  });

});