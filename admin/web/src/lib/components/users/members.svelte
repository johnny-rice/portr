<script lang="ts">
  import DataTable from "$lib/components/data-table.svelte";
  import { Button } from "$lib/components/ui/button";
  import InviteUser from "$lib/components/users/invite-user.svelte";
  import { currentUser, users, usersLoading } from "$lib/store";
  import type { TeamUser } from "$lib/types";
  import { updateQueryParam } from "$lib/utils";
  import { getContext, onMount } from "svelte";
  // @ts-expect-error
  import { createRender, createTable } from "svelte-headless-table";
  import { writable } from "svelte/store";
  import Pagination from "../Pagination.svelte";
  import Avatar from "./avatar.svelte";
  import Delete from "./delete.svelte";
  import UserEmail from "./user-email.svelte";
  import { UserPlus } from "lucide-svelte";

  let addMemberModalOpen = false;

  const urlParams = new URLSearchParams(window.location.search);

  let pageNo = writable(1);
  let pageNoStr = urlParams.get("page") || "1";
  pageNo.set(parseInt(pageNoStr, 10) || 1);

  $: updateQueryParam(urlParams, "page", $pageNo.toString());
  $: getUsers($pageNo.toString());

  let team = getContext("team") as string;

  let totalItems = 0;

  const getUsers = async (pageNo: string = "1") => {
    usersLoading.set(true);
    try {
      const response = await fetch(
        `/api/v1/team/users?page=${pageNo}&page_size=10`,
        {
          headers: {
            "x-team-slug": team,
          },
        }
      );
      const resp = await response.json();
      users.set(resp["data"]);
      totalItems = resp["count"];
    } catch (err) {
      console.error(err);
    } finally {
      usersLoading.set(false);
    }
  };

  const table = createTable(users);

  const columns = table.createColumns([
    table.column({
      header: "Email",
      accessor: (item: TeamUser) => item,
      cell: (item: any) =>
        createRender(UserEmail, {
          email: item.value.user.email,
          is_superuser: item.value.user.is_superuser,
        }),
    }),
    table.column({
      header: "Role",
      accessor: (item: TeamUser) => item.role,
    }),
    table.column({
      accessor: (item: TeamUser) => item,
      header: "Avatar",
      cell: (item: any) =>
        createRender(Avatar, {
          url: item.value.user.github_user?.github_avatar_url,
          fallback: item.value.user.email,
        }),
    }),
    table.column({
      accessor: (item: TeamUser) => item,
      header: "",
      cell: (item: any) =>
        createRender(Delete, {
          user: item.value,
        }),
    }),
  ]);

  onMount(() => {
    getUsers();
  });
</script>

<InviteUser bind:open={addMemberModalOpen} />

<div class="flex w-full justify-between items-center mb-4">
  <div>
    <Button
      on:click={() => (addMemberModalOpen = !addMemberModalOpen)}
      disabled={$currentUser?.role === "member"}
      class="flex items-center gap-2"
    >
      <UserPlus class="h-4 w-4" />
      Add member
    </Button>
  </div>
  <div>
    <Pagination count={totalItems} perPage={10} currentPage={pageNo} />
  </div>
</div>

<DataTable
  {table}
  {columns}
  isLoading={$usersLoading}
  noCard={true}
/>
