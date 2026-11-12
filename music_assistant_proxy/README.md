# Music Assistant Proxy

<img src="icon.png" width="96" align="right" alt="">

Music Assistant running on **its own hardware**, in your Home Assistant sidebar.

Music Assistant's own add-on runs the server on your Home Assistant machine. If you
would rather run it on dedicated hardware — a NAS, a mini PC, anything with the
headroom for library scans and transcoding — you lose the sidebar panel, because
Ingress only serves add-ons.

This add-on is an nginx reverse proxy that gives it back. It does **not** run Music
Assistant; it puts a server running elsewhere behind Home Assistant's Ingress, so the
panel appears in the sidebar and is reachable wherever Home Assistant is, without
exposing Music Assistant itself.

It also works around a quirk of the current Music Assistant release, which decides it
is running as an add-on purely from the URL and then refuses to show a login form.
[The add-on docs](DOCS.md) explain what is rewritten and why,
how signing in works, and what to expect when Music Assistant updates.

## Install

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

[![Open your Home Assistant instance and show the dashboard of an add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=music_assistant_proxy&repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

1. **Add repository** with the first button (or *Settings → Add-ons → Add-on Store
   → ⋮ → Repositories*).
2. **Open the add-on** with the second button, then *Install*.
3. Fill in the options below, *Start*, and enable *Show in sidebar*.

## Options

| Option | Default | What it is |
| :-- | :-- | :-- |
| `server_host` | `192.168.1.11` | Address of the Music Assistant server: an IP, a hostname, or a full URL such as `https://ma.example.com`. |
| `server_port` | `8095` | Port of the Music Assistant web interface (`443` for an HTTPS URL). |
| `ma_users` | _(empty)_ | Optional per-person auto-login: Home Assistant username → that person's Music Assistant token. See below. |
| `ma_token` | _(empty)_ | Optional shared auto-login token for everyone not in `ma_users`. See below. |

## Several people, each with their own Music Assistant account

The panel shows for every Home Assistant user, admins and standard users alike. What it
cannot do on its own is sign each person into *their* Music Assistant account.

**Why a manual mapping is needed.** When Music Assistant runs as an add-on on the Home
Assistant machine, it trusts Home Assistant to say who is signed in, so everyone lands in
their own account automatically. That trust only exists on Home Assistant's internal
network; Music Assistant checks it at the connection level, not just from a header. A
server on its own hardware has no such link: it only trusts its own users and tokens.
Home Assistant does still tell this add-on who opened the panel, so the add-on can hand
Music Assistant the right token, but someone has to tell it which token belongs to whom.

<img src="https://raw.githubusercontent.com/shuricksumy/home-assistant-apps/main/music_assistant_proxy/images/ma-users-flow.svg" alt="Anna opens the panel; Home Assistant tells the add-on she is signed in; the add-on looks up anna in ma_users and passes her token to Music Assistant, which signs her in as anna" width="880">

You have two options:

- **Each person signs in once.** Leave the token options empty. Each person opens the
  panel and signs in with their Music Assistant account. The session is kept per browser
  for 30 days and renews while it is used.
- **Map Home Assistant users to Music Assistant tokens.** Nobody has to sign in. Set it up
  as below.

**Setting up the mapping**

1. **Create a token for each person in Music Assistant.** Sign in to Music Assistant *as
   that person*, open the profile settings, create a **long-lived token**, and copy it.
   The token decides which Music Assistant account they get, so it must come from their
   own account.
2. **Find each person's Home Assistant username.** It is the name typed at the login
   screen, not the display name. With Advanced Mode on in your profile, it is shown under
   **Settings → People → Users**. Case does not matter.
3. **Add the mapping to the add-on.** Open **Settings → Add-ons → Music Assistant Proxy →
   Configuration**. Under **Per-user sign-in**, add one entry per person with their
   **Home Assistant username** and **Music Assistant token**, then **Save**. Entries can
   be edited or removed there later.

   If you prefer YAML, choose **⋮ → Edit in YAML** and add an `ma_users` list instead:

   ```yaml
   ma_users:
     - ha_user: alex
       ma_token: "<alex's long-lived token>"
     - ha_user: anna
       ma_token: "<anna's long-lived token>"
   ```

   <img src="https://raw.githubusercontent.com/shuricksumy/home-assistant-apps/main/music_assistant_proxy/images/ma-users-config.svg" alt="The add-on Configuration tab in YAML mode with ma_users listing alex and anna, each with a token" width="640">

   Only Home Assistant admins can open this tab, so the list of tokens is not visible to
   anyone else.
4. **Save and restart the add-on,** then open the **Log** tab. Every entry is checked
   against Music Assistant:

   ```
   ma_users: alex: token accepted (Music Assistant user "alex")
   ma_users: anna: Music Assistant rejected the token (HTTP 401).
   ```

   A rejected token, a misspelt username or a duplicate entry is reported there.
5. **Each person opens the Music Assistant panel** and lands in their own account.

People who are not listed get the normal Music Assistant login page. When a person is
added or removed, or their token changes, edit the list and restart the add-on.

The add-on still accepts a single shared `ma_token`, but it signs every unlisted person in
as the one Music Assistant user who owns it, and anyone it is given to can read it from the
page. In a shared household, use `ma_users` instead. [The add-on docs](DOCS.md#auto-login)
have the details.

## License

MIT — see [LICENSE](../LICENSE).
